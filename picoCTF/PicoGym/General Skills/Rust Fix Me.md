---
tags: [picoctf, general-skills, rust, memory-safety]
platform: picoCTF
category: General Skills
---
Covers: Rust Fix Me 1, Rust Fix Me 2, Rust fix me3.

## Rust Fix Me 1
`cargo build` reports the actual problems directly:
1. Missing `;` on line 5, add it.
2. Printing a variable needs `{}` as a placeholder: `println!("Decrypted flag: {}", String::from_utf8_lossy(&decrypted_buffer));`
3. `ret` should be `return`.

Then `cargo build` succeeds and `cargo run` works.

## Rust Fix Me 2
`cargo build` says to make `borrowed_string` mutable by adding `mut`. Same fix needed for `party_foul` in the last two lines. Then it builds and runs.

## Rust fix me3
The easiest of the [[Three challenge|three]]: the compiler error itself tells you the fix, just uncomment the `unsafe{}` block.

## Why
See [[Memory Safety in Rust]]. Rust's compiler enforces its ownership/mutability rules at compile time, so a "broken" Rust program here isn't subtly wrong at runtime, it's one the compiler already refuses to build, with an error message naming the exact rule violated. `mut` makes intentional mutation explicit (variables are immutable by default), and `unsafe{}` is how Rust lets you opt out of some compile-time checks for operations the compiler can't prove safe on its own, explicit and visible rather than a silent default.
