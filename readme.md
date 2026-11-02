## 🛠️ Project Bootstrap Checklist (Maintainer Only)

When creating a new project from this template under **SID-LabX**:

### 1. Create the Repo
- Click **Use this template** ➔ Set Owner to **`SID-LabX`**.
- Make your first push to `main` (the `init-signatures` bot will automatically create the `signatures` branch).

### 2. Lock the `main` Branch (30 Seconds)
1. Go to repository **Settings** ➔ **Branches** ➔ Click **Add branch protection rule**.
2. **Branch name pattern:** `main`
3. Check **"Require a pull request before merging"**.
4. Uncheck **"Require approvals"** (so you can merge your own code).
5. Check **"Require status checks to pass before merging"** ➔ search and select **`CLAAssistant`**.
6. Click **Save changes**.

> [!NOTE]
> All other security settings (Secret Scanning, Push Protection, Dependabot, CodeQL, and CLA enforcement) are 100% automatic and inherited from `SID-LabX`!

---

# Project Name

A brief description of what this project does.

## Contributing

We welcome contributions! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and note that all contributors must sign our [Contributor License Agreement (CLA)](CLA.md) before pull requests can be merged.

## License

This project is licensed under the terms of the [PROPRIETARY SOURCE-AVAILABLE LICENSE](LICENSE).


---
