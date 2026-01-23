# Infra and bootstrap

Use the scripts in this folder to bootstrap VMs (Ubuntu 22.04+).

Steps (summary):
1. Create 3 Ubuntu VMs on Azure (frontend, backend, db) in same VNet.
2. Copy `infra/bootstrap-*.sh` to each VM and run them.
3. Configure nginx on frontend (copy `infra/nginx-frontend.conf`) and replace BACKEND_PRIVATE_IP.
4. On backend VM create a python venv, install requirements, and configure systemd service (sample provided).
5. Add your SSH public key to GitHub Actions secrets and repo secrets:
   - `DEPLOY_SSH_KEY` (private key)
   - `FRONTEND_HOST`, `BACKEND_HOST`, `DEPLOY_SSH_USER`

This repo includes GitHub Actions to SCP artifacts and restart services.
