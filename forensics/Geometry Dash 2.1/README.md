# Geometry Dash 2.1

- The `cclocallevels` can be decrypted by looking through old GD docs on Github, and finding that:

  - XORing with **11**
  - Base64 decoding the result
  - Ungzipping it
  - This reveals an XML file.

- The XML file contains a **Base64** message that says "the flag is in the level."

  - Nearby, there's a `level` string that's also **Base64** encoded and gzipped.

- After decoding and ungzipping the `level` string, it reveals a list of objects.

- The old GD docs mention a **Base64** message that says "the text below consists of multiple text objects," meaning multiple objects together form a message.

- The GD docs show that text objects have the property **"31"**, corresponding to the "text" property.

  - Filtering for these objects gives the message: **"perhaps try 95484635."**

- The number **95484635** is a level ID.
  - Checking this level ID in Geometry Dash or on **gdbrowser.com** shows the flag in the comments section.
