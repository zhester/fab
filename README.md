fab
===

Yet Another Build System

Introduction
============

There are a lot of high-quality build systems around.  Particularly useful are
the meta-build systems like CMake.  This is an attempt at a stand-alone
build system with no dependencies (other than a Python interpreter).

Why?
----

Where I work, we have a very limited and controlled system of adding tools to
a software project.  It's either a universal (and usually universally awful)
tool, or it's painful to make work across every computer that needs to run the
tool.

In the case of build systems, we have several competing proprietary and one
open source system in place.  None of them work well.  Modern variations on
the ubiquitous `make` are not consistent and widespread enough (e.g. for
Windows) to allow me to use the system that makes me the most productive.

The one thing I know will be available everywhere is Python.  After that
nothing is assumed (included packages or even the underlying operating
system).

Features and Requirements
-------------------------

- Built-in dependency graph generation
  - I work with compilers that produce incompatible dependency graphs
  - IWYU isn't 100% in place, but reasonably in reach for most projects
  - The generator should be able to work as a stand-alone tool
- Meta-build support
  - GNU Make Makefile output
  - MS Visual Studio solution output
- Version control support
  - Understands a little about VCS context (e.g. Git and Subversion
    repositories)
  - Can enforce versioning checks for both tools and source code
- Environment control
  - Can use controlled environments (e.g. like a virtual environment wrapper),
    or completely take control of the environment to ensure consistency across
    all hosts
- Switch control, integrity, transparency
  - Compiler/assembler/preprocessor switches must be easily controlled and
    auditable for integrity
  - Even if the switches are dynamically generated, actual usage can be
    captured, and tested for integrity to make sure some hosts are not
    changing switches
- Intelligently handles variations in project/library directory layouts
- Flexible configuration
  - Projects can be configured 100% automatically (if desired)
  - Projects can be configured declaratively (like most build systems)
  - Projects can be configured imperatively (by writing actual code)
  - Projects can be configured using any combination of the previous 3
  - Directories within projects can maintain an isolated context without
    affecting other directories
- No assumed compilers
- No assumed libraries
- Not necessarily a software build system
  - Expected to also be used to generate documentation
  - Pre-generated web content from non-web source documents

