<table class="table table-striped">
<tr>
<th>Name</th>
<th>Type</th>
<th>Inclusion</th>
<th>Description</th>
</tr>
<tr>
<td><code>module_id</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>The module ID, which includes either the module <a href="/operate/modules/other-hardware/naming-modules/#create-a-namespace-for-your-organization">namespace</a> or organization ID, followed by its name.
<div class="alert alert-caution" role="alert">
<h4 class="alert-heading">Caution</h4>

<p>The <code>module_id</code> uniquely identifies your module.
Do not change the <code>module_id</code>.</p>

</div>
</td>

</tr>
<tr>
<td><code>visibility</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>Whether the module is accessible only to members of your <a href="/manage/reference/organize/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can later make a private module public using the <code>viam module update</code> command. Once you make a module public, you can change it back to private if it is not configured on any machines outside of your organization.</td>
</tr>
<tr>
<td><code>url</code></td>
<td>string</td>
<td><strong>Required</strong> for cloud build</td>
<td>The URL of the GitHub repository containing the source code of the module. Cloud build will fail if you do not provide this. Optional for local modules.</td>
</tr>
<tr>
<td><code>description</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>A description of your module and what it provides.</td>
</tr>
<tr>
<td><code>models</code></td>
<td>array</td>
<td>Optional</td>
<td><p>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model in the models array or one application in the applications array. A model consists of an <code>api</code> and <code>model</code> key pair. If you are publishing a public module (<code>"visibility": "public"</code>), the namespace of your model must match the <a href="/operate/modules/other-hardware/naming-modules/#create-a-namespace-for-your-organization">namespace of your organization</a>.</p>
<p>You are strongly encouraged to include a <code>markdown_link</code> to the section of the README containing configuration information about each model, so that the section will be displayed alongside the configuration panel when configuring the model. For example, <code>"README.md#configure-your-meteo_pm-sensor"</code>. Please also include a <code>short_description</code> describing what hardware the model supports.</p></td>
</tr>
<tr>
<td><code>entrypoint</code></td>
<td>string</td>
<td>Optional</td>
<td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program. If you are providing your module as a single file to the <code>upload</code> command, provide the path to that single file. If you are providing a directory containing your module to the <code>upload</code> command, provide the path to the entry point file contained within that directory. Required if you are shipping a model.</td>
</tr>
<tr>
<td><code>build</code></td>
<td>object</td>
<td>Optional</td>
<td>An object containing the command to run to build your module, as well as optional fields for the path to your dependency setup script, the target architectures to build for, and the path to your built module. Use this with the <a href="/dev/tools/cli/#using-the-build-subcommand">Viam CLI's build subcommand</a>.<br><ul><li><code>"setup"</code> (Optional): Command to run for setting up the build environment.</li><li><code>"build"</code> (Required): Command to run to build the module tarball.</li><li><code>"path"</code> (Optional): Path to the build module tarball.</li>
<li><code>"arch"</code> (Required): Array of architectures to build for. For more information see <a href="/operate/modules/other-hardware/manage-modules/#supported-platforms-for-automatic-updates">Supported platforms for automatic updates</a>.</li><li><code>"darwin_deps"</code> (Required): Array of homebrew dependencies for Darwin builds. Explicitly pass <code>[]</code> for empty. Default: <code>["go", "pkg-config", "nlopt-static", "x264", "jpeg-turbo", "ffmpeg"]</code></li></ul></td>
</tr>
<tr>
<td><code>markdown_link</code></td>
<td>string</td>
<td>Optional</td>
<td>Link to the documentation (README) for this module. Viam uses this to render your README on your module's page in the <a href="https://app.viam.com/registry">registry</a>. Similar to the <code>markdown_link</code> within the <code>models</code> object (described above), which allows the app to render info for a specific model in the configuration panel.</td>
</tr>
<tr>
<td><code>$schema</code></td>
<td>string</td>
<td>Optional</td>
<td>Enables VS Code hover and autocomplete as you edit your module code. Gets auto-generated when you run <code>viam module generate</code> or <code>viam module create</code>. Has no impact on the module's function.</td>
</tr>
<tr>
<td><code>applications</code></td>
<td>array</td>
<td>Optional</td>
<td>Objects that provide information about the <a href="/operate/control/viam-applications/">applications</a> provided by the module.</td>
</tr>

</table>
