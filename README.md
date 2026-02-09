# Kubernetes CI Image Pipeline

This repository demonstrates a CI-driven workflow for building, tagging,
publishing, and cleaning up OS images used in Kubernetes CI pipelines.

The design is inspired by real-world CI challenges in Kubernetes projects, where OS images must be reproducible, release-aware,
and low-maintenance for project maintainers.

---

## Structure
kubernetes-ci-image-pipeline/
├── .gitlab-ci.yml
├── ci/
│   ├── build-images.yml        # CI job definition for building and publishing images
│   └── cleanup-images.yml      # CI job definition for cleaning up unused images
├── scripts/
│   ├── build_images.py         # Image build and tagging logic
│   └── cleanup_registry.py     # Registry cleanup and retention policy logic
├── config/
│   └── images.yml              # Declarative OS image matrix used by CI
├── Dockerfile                  # Image builder runtime environment
├── README.md                   # Project overview and design documentation



## Problem Statement

Many Kubernetes projects rely on pre-built OS images for CI testing.
When these images are created manually, they become a bottleneck:
- Maintainers must be available to build and push images
- Cleanup is often inconsistent or risky
- Release branches complicate image retention policies

This repository demonstrates how those problems can be solved with
automation.

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

## Image Tagging Strategy

Images are published with two tags:

- Immutable hash-based tag  
- Mutable `latest` tag for convenience

This ensures reproducibility while remaining easy to consume in CI.

---

## Cleanup Strategy

Cleanup runs only on scheduled pipelines and:
- Retains images referenced by supported branches
- Deletes images older than a defined retention window
- Supports dry-run mode for safety

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
