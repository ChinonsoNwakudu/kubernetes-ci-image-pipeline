# Kubernetes CI Image Pipeline

# Kubernetes CI Image Pipeline

This repository demonstrates a CI-driven workflow for building, tagging, publishing,
and cleaning up operating system images used in Kubernetes-related CI environments.

The project is inspired by real-world needs in Kubespray and Kubernetes test-infra,
where CI pipelines rely on prebuilt OS images for reproducible, deterministic testing.
Today, many of these images are created and maintained manually, which introduces
operational bottlenecks and unnecessary maintainer toil.

This repository explores how that process can be automated in a clean, auditable,
and release-aware way using CI pipelines.


---

## Structure
```
kubernetes-ci-image-pipeline/
├── .gitlab-ci.yml
├── ci/
│   ├── build-images.yml
│   └── cleanup-images.yml
├── scripts/
│   ├── build_images.py
│   └── cleanup_registry.py
├── config/
│   └── images.yml
├── Dockerfile
└── README.md
```               



## Problem Statement

Many Kubernetes projects rely on pre-built OS images for CI testing.
When these images are created manually, they become a bottleneck:
- Maintainers must be available to build and push images
- Cleanup is often inconsistent or risky
- Release branches complicate image retention policies

This creates several issues:

- CI can be blocked when maintainers are unavailable
- Image build processes are tribal knowledge
- Old images accumulate without clear retention policies
- Release branches require images that are no longer used by `main` or `master`



This repository proposes a CI-native approach that removes these bottlenecks.

---

## Key Design Goals

- **Automated image builds** triggered by configuration changes
- **Deterministic tagging** for reproducibility
- **Release-aware cleanup policies**
- **Minimal maintainer intervention**
- **Safety-first operations (dry-run, allowlists)**

---

## CI Workflow Overview

1. Validate image definitions
2. Build OS images automatically
3. Push images to a container registry
4. Periodically clean up unused images while retaining those required
   for supported release branches

---

Image definitions live in `config/images.yml`, not inside CI scripts.

This makes the system:
- Easier to review
- Easier to extend
- Less error-prone than hardcoded pipelines

CI consumes configuration; it does not define it.


CI configuration and execution logic are intentionally split:

- `ci/` defines pipeline orchestration
- `scripts/` contains the implementation logic

This mirrors patterns used in Kubernetes test-infra and prevents CI files
from becoming unreviewable monoliths.

## Image Tagging Strategy

Images are published with two tags:

- Immutable hash-based tag  
- Mutable `latest` tag for convenience

This ensures reproducibility while remaining easy to consume in CI.

Images are built with deterministic tagging based on:

- Distribution
- Version
- Build metadata (e.g. commit SHA or pipeline ID)

This ensures CI runs are traceable and debuggable.


---

## Cleanup Strategy

Cleanup runs only on scheduled pipelines and:
- Retains images referenced by supported branches
- Deletes images older than a defined retention window
- Supports dry-run mode for safety

---

## Design Principles

This project is intentionally designed around principles commonly used in
Kubernetes and CNCF subprojects.

---

## What This Project Is Not

- A full production registry implementation
- A replacement for Kubernetes test-infra tooling

Instead, it focuses on clarity, correctness, and maintainability.

---

## Why This Matters

CI infrastructure should be boring, predictable, and easy to maintain.
By automating image pipelines, projects can reduce operational toil
and focus on delivering value to users.
