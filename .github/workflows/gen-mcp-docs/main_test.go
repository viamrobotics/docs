package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// writeFiles lays out a fixture package (or packages) under a temp app root and returns its path.
// files is keyed by path relative to the app root, e.g. "mcpserver/tools.go" or "data/models.go".
func writeFiles(t *testing.T, files map[string]string) string {
	t.Helper()
	root := t.TempDir()
	for rel, content := range files {
		path := filepath.Join(root, rel)
		if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
	}
	return root
}

const helperSrc = `package mcpserver

func addTool(s int, tool *toolT, timeout int, h int) {}

type toolT struct{}

func readOnlyTool(name, title, description string) *toolT { return &toolT{} }
func writeTool(name, title, description string, destructive bool) *toolT { return &toolT{} }
func machineTool(name, title, description string) *toolT { return &toolT{} }
`

func TestExtractTools_Basics(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/tools.go": `package mcpserver

const readDescription = "Read something. " +
	"Multi-line, like the real ones."

func register() {
	addTool(0, readOnlyTool("read_thing", "Read thing", readDescription), 0, 0)
	addTool(0, writeTool("add_thing", "Add thing", "Adds a thing.", false), 0, 0)
	addTool(0, writeTool("delete_thing", "Delete thing", "Deletes a thing.", true), 0, 0)
	addTool(0, machineTool("call_thing", "Call thing", "Calls a live thing."), 0, 0)
}
`,
	})

	tools, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err != nil {
		t.Fatalf("extractTools: %v", err)
	}
	if len(tools) != 4 {
		t.Fatalf("got %d tools, want 4: %+v", len(tools), tools)
	}

	want := map[string]struct {
		category    string
		description string
	}{
		"read_thing":   {categoryReadOnly, "Read something. Multi-line, like the real ones."},
		"add_thing":    {categoryWrite, "Adds a thing."},
		"delete_thing": {categoryDestroy, "Deletes a thing."},
		"call_thing":   {categoryLiveMachine, "Calls a live thing."},
	}
	for _, got := range tools {
		w, ok := want[got.Name]
		if !ok {
			t.Errorf("unexpected tool %q", got.Name)
			continue
		}
		if got.Category != w.category {
			t.Errorf("%s: category = %q, want %q", got.Name, got.Category, w.category)
		}
		if got.Description != w.description {
			t.Errorf("%s: description = %q, want %q", got.Name, got.Description, w.description)
		}
	}
}

func TestExtractTools_SortOrder(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/tools.go": `package mcpserver

func register() {
	addTool(0, machineTool("z_machine", "t", "d"), 0, 0)
	addTool(0, writeTool("z_destroy", "t", "d", true), 0, 0)
	addTool(0, writeTool("a_write", "t", "d", false), 0, 0)
	addTool(0, readOnlyTool("z_read", "t", "d"), 0, 0)
	addTool(0, readOnlyTool("a_read", "t", "d"), 0, 0)
}
`,
	})

	tools, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err != nil {
		t.Fatalf("extractTools: %v", err)
	}
	var gotOrder []string
	for _, tl := range tools {
		gotOrder = append(gotOrder, tl.Name)
	}
	wantOrder := []string{"a_read", "z_read", "a_write", "z_destroy", "z_machine"}
	if strings.Join(gotOrder, ",") != strings.Join(wantOrder, ",") {
		t.Errorf("order = %v, want %v", gotOrder, wantOrder)
	}
}

func TestExtractTools_CrossPackageArithmetic(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/tools.go": `package mcpserver

import (
	"strconv"

	"github.com/viamrobotics/app/data"
)

var thingDescription = "Online means the part reported within the last " +
	strconv.Itoa(data.LiveThresholdMS/1000) + " seconds."

func register() {
	addTool(0, readOnlyTool("read_thing", "Read thing", thingDescription), 0, 0)
}
`,
		"data/models.go": `package data

const LiveThresholdMS = 10000
`,
	})

	tools, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err != nil {
		t.Fatalf("extractTools: %v", err)
	}
	if len(tools) != 1 {
		t.Fatalf("got %d tools, want 1", len(tools))
	}
	want := "Online means the part reported within the last 10 seconds."
	if tools[0].Description != want {
		t.Errorf("description = %q, want %q", tools[0].Description, want)
	}
}

func TestExtractTools_UnrecognizedConstructorFailsLoudly(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/tools.go": `package mcpserver

func someNewTool(name, title, description string) *toolT { return &toolT{} }

func register() {
	addTool(0, someNewTool("mystery", "Mystery", "A new kind of tool."), 0, 0)
}
`,
	})

	_, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err == nil {
		t.Fatal("expected an error for an unrecognized tool constructor, got nil")
	}
	if !strings.Contains(err.Error(), "someNewTool") {
		t.Errorf("error %q does not name the unrecognized constructor", err)
	}
}

// TestExtractTools_PerFileAliasScoping guards against a global, package-wide alias table: two
// files in the same package are free to alias two different imports the same way (Go import
// aliases are scoped per file), and mcpserver's own source already does this in practice ("v3"
// aliases both github.com/robfig/cron/v3 and github.com/Masterminds/semver/v3 depending on the
// file). Here, two files both alias a sibling package "internal", but to two different sibling
// packages. A global, last-write-wins table would resolve both files' references through whichever
// import happened to be inserted last, silently producing the wrong value for one of them instead
// of failing -- worse than an error, since nothing would flag it.
func TestExtractTools_PerFileAliasScoping(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/a.go": `package mcpserver

import internal "github.com/viamrobotics/app/internal_a"

var aDescription = "A bound: " + internal.Value

func registerA() {
	addTool(0, readOnlyTool("read_a", "Read A", aDescription), 0, 0)
}
`,
		"mcpserver/b.go": `package mcpserver

import internal "github.com/viamrobotics/app/internal_b"

var bDescription = "B bound: " + internal.Value

func registerB() {
	addTool(0, readOnlyTool("read_b", "Read B", bDescription), 0, 0)
}
`,
		"internal_a/values.go": "package internal_a\n\nconst Value = \"A42\"\n",
		"internal_b/values.go": "package internal_b\n\nconst Value = \"B99\"\n",
	})

	tools, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err != nil {
		t.Fatalf("extractTools: %v", err)
	}
	byName := map[string]tool{}
	for _, tl := range tools {
		byName[tl.Name] = tl
	}
	if got, want := byName["read_a"].Description, "A bound: A42"; got != want {
		t.Errorf("read_a description = %q, want %q (a package-wide alias table would leak b.go's \"internal\" into a.go)", got, want)
	}
	if got, want := byName["read_b"].Description, "B bound: B99"; got != want {
		t.Errorf("read_b description = %q, want %q (a package-wide alias table would leak a.go's \"internal\" into b.go)", got, want)
	}
}

func TestExtractTools_ExternalPackageRefused(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/tools.go": `package mcpserver

import (
	"strconv"

	"some/external/pkg"
)

var thingDescription = "Bound: " + strconv.Itoa(pkg.SomeLimit) + "."

func register() {
	addTool(0, readOnlyTool("read_thing", "Read thing", thingDescription), 0, 0)
}
`,
	})

	_, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err == nil {
		t.Fatal("expected an error for a reference into an external package, got nil")
	}
	if !strings.Contains(err.Error(), "some/external/pkg") {
		t.Errorf("error %q does not name the external package", err)
	}
}

func TestExtractTools_NoTools(t *testing.T) {
	root := writeFiles(t, map[string]string{
		"mcpserver/helpers.go": helperSrc,
		"mcpserver/empty.go":   "package mcpserver\n",
	})

	_, err := extractTools(filepath.Join(root, "mcpserver"), root)
	if err == nil {
		t.Fatal("expected an error when no tools are found, got nil")
	}
}

func TestCodeSpanURLs(t *testing.T) {
	cases := []struct{ in, want string }{
		{"see (https://docs.viam.com/reference/apis/), such as", "see (`https://docs.viam.com/reference/apis/`), such as"},
		{"no urls here", "no urls here"},
		{"trailing period at https://example.com/x.", "trailing period at `https://example.com/x`."},
	}
	for _, c := range cases {
		if got := codeSpanURLs(c.in); got != c.want {
			t.Errorf("codeSpanURLs(%q) = %q, want %q", c.in, got, c.want)
		}
	}
}

func TestWriteTable(t *testing.T) {
	dir := t.TempDir()
	out := filepath.Join(dir, "nested", "table.md")
	tools := []tool{
		{Name: "a_tool", Category: categoryReadOnly, Description: "Does a thing | with a pipe."},
	}
	if err := writeTable(out, tools); err != nil {
		t.Fatalf("writeTable: %v", err)
	}
	got, err := os.ReadFile(out)
	if err != nil {
		t.Fatal(err)
	}
	want := "<!-- prettier-ignore -->\n" +
		"| Tool | Category | Description |\n" +
		"| ---- | -------- | ----------- |\n" +
		"| `a_tool` | Read-only | Does a thing \\| with a pipe. |\n"
	if string(got) != want {
		t.Errorf("writeTable output =\n%s\nwant\n%s", got, want)
	}
}
