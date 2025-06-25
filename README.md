# GSAM Compiler

GSAM (Graph Script Ain't Markup) is a simple, scripting language designed for creating and executing logic flows through a component-based syntax. It powers scripting via minimal, readable components that map easily to visual nodes — perfect for both beginners and experienced developers building logic-driven applications.

# 📘 What is GSAM?

GSAM is a scripting language that emphasizes visual logic and node-based workflows. It is meant to be easily parseable, human-readable, and extensible, designed primarily for use in scripting engines or tools like GraphScript.

Think of it like writing logic in blocks, but as text.

# 🔤 Example Syntax (Hello World)

```
output
 "Hello, World!"
 endline
```

# 📦 Installing the GSAM Compiler

Make sure you have Python 3.8+ installed.

## Using `pipx`

You can install GSAM globally using pipx:

```bash
pipx install gsam
```

## Using `pip`

You can also install GSAM using pip:

```bash
pip install gsam
```

# ▶️ Running a GSAM Script

Once installed, run any .gsam file like this:

```bash
gsamc path/to/your_file.gsam
```

If you want to test quickly:

```bash
echo 'output\n "Hi!"\n endline' > test.gsam
gsamc test.gsam
```

