#!/usr/bin/env python3
"""
Verify SVG diagram layout: nesting, balance, and text fitting.
Run after every SVG edit before presenting to reviewer.

Usage: python3 scripts/verify-svg.py static/what-is-viam-technical.svg
"""

import re
import sys
from collections import defaultdict


def parse_rects(svg_content):
    """Extract all rects with their x, y, width, height."""
    rects = []
    # Match rect elements, capturing the line they're on
    for i, line in enumerate(svg_content.split('\n')):
        match = re.search(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"', line)
        if match:
            x, y, w, h = float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4))
            # Try to find a comment or nearby text for labeling
            rects.append({
                'x': x, 'y': y, 'w': w, 'h': h,
                'right': x + w, 'bottom': y + h,
                'line': i + 1,
                'src': line.strip()[:80]
            })
    return rects


def parse_texts(svg_content):
    """Extract all text elements with position and content."""
    texts = []
    for i, line in enumerate(svg_content.split('\n')):
        match = re.search(r'<text\s+x="([^"]+)".*?font-size:(\d+)px.*?>([^<]+)</text>', line)
        if match:
            x = float(match.group(1))
            font_size = int(match.group(2))
            content = match.group(3).strip()
            # Estimate pixel width: bold ~7px/char at 13px, normal ~6px/char at 10-11px, italic ~5.5px/char at 9px
            if font_size >= 13:
                px_per_char = 7.5
            elif font_size >= 10:
                px_per_char = 6.0
            else:
                px_per_char = 5.5
            est_width = len(content) * px_per_char
            texts.append({
                'x': x, 'font_size': font_size, 'content': content,
                'est_width': est_width, 'line': i + 1
            })
    return texts


def check_nesting(rects):
    """Check that smaller rects fit inside larger rects that share similar x positions."""
    issues = []
    # Sort by area (largest first)
    by_area = sorted(rects, key=lambda r: r['w'] * r['h'], reverse=True)

    for i, child in enumerate(by_area):
        for parent in by_area:
            if parent is child:
                continue
            # Check if child is roughly inside parent (overlapping y range and similar x)
            if (child['x'] >= parent['x'] - 5 and
                child['y'] >= parent['y'] and
                child['w'] < parent['w'] and
                child['bottom'] <= parent['bottom'] + 5):
                # This looks like a parent-child relationship
                if child['right'] > parent['right']:
                    issues.append(
                        f"  OVERFLOW: rect at line {child['line']} (right={child['right']:.0f}) "
                        f"exceeds parent at line {parent['line']} (right={parent['right']:.0f}) "
                        f"by {child['right'] - parent['right']:.0f}px"
                    )
                # Check horizontal balance
                left_pad = child['x'] - parent['x']
                right_pad = parent['right'] - child['right']
                if abs(left_pad - right_pad) > 3 and left_pad > 0 and right_pad > 0:
                    issues.append(
                        f"  UNBALANCED: rect at line {child['line']} in parent at line {parent['line']}: "
                        f"left={left_pad:.0f}px right={right_pad:.0f}px (diff={abs(left_pad-right_pad):.0f}px)"
                    )
                break  # Only check immediate parent
    return issues


def check_text_overflow(texts, rects):
    """Check if text is wider than its containing rect."""
    issues = []
    for text in texts:
        # Find the smallest rect that contains this text
        containing = None
        for rect in rects:
            if (rect['x'] <= text['x'] <= rect['right'] and
                rect['y'] <= 400):  # rough y check
                if containing is None or rect['w'] < containing['w']:
                    containing = rect
        if containing and text['est_width'] > containing['w']:
            issues.append(
                f"  TEXT OVERFLOW: \"{text['content']}\" (~{text['est_width']:.0f}px) "
                f"in rect width={containing['w']:.0f}px at line {containing['line']}"
            )
    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify-svg.py <svg-file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        content = f.read()

    rects = parse_rects(content)
    texts = parse_texts(content)

    print(f"Found {len(rects)} rects, {len(texts)} text elements\n")

    print("=== Nesting & Balance ===")
    nesting_issues = check_nesting(rects)
    if nesting_issues:
        for issue in nesting_issues:
            print(issue)
    else:
        print("  All rects properly nested and balanced")

    print("\n=== Text Overflow ===")
    text_issues = check_text_overflow(texts, rects)
    if text_issues:
        for issue in text_issues:
            print(issue)
    else:
        print("  No text overflow detected")

    print()
    if nesting_issues or text_issues:
        print(f"ISSUES FOUND: {len(nesting_issues)} nesting, {len(text_issues)} text")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
