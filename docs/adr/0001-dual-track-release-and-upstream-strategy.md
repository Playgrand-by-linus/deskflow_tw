# Dual-Track Release and Upstream Contribution Strategy

We decided to adopt a dual-track strategy for Deskflow Traditional Chinese edition: maintaining an independent distribution with automated CI/CD builds on `Playgrand-by-linus/deskflow_tw` while concurrently preparing Pull Requests for upstream `deskflow/deskflow`.

## Context

Deskflow upstream currently lacks Traditional Chinese (`zh_TW`) support. Upstream PR review cycles may take weeks or months. Maintaining automated GitHub Actions builds provides immediate, pre-compiled releases (.msi, .dmg) for the community without waiting for upstream merges, while preserving clean commits suitable for direct upstream merging.
