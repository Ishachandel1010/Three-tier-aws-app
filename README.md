# Three-Tier Web Application on AWS

A simple message board app demonstrating a classic three-tier architecture — Presentation, Application, and Database — fully containerized with Docker Compose and deployed on an AWS EC2 (Ubuntu) instance inside a custom VPC.

![App Screenshot](screenshots/screenshot.png)

## Architecture

Internet
|
v
[ Nginx ] <-- Tier 1: Presentation (reverse proxy, port 80)
|
v
[ Flask + Gunicorn ] <-- Tier 2: Application (business logic, port 5000)
|
v
[ PostgreSQL ] <-- Tier 3: Database (persistent storage, port 5432)


Each tier runs in its own Docker container, connected via a private Docker network created automatically by Docker Compose. Only Nginx exposes a port to the outside world (80) — the app and database tiers are not directly reachable from the internet, mirroring how production three-tier apps are secured.

## AWS Infrastructure

This app runs on an Ubuntu EC2 instance inside a custom VPC:

- **VPC** with a public subnet
- **Internet Gateway** attached, with route table configured for public internet access
- **EC2 instance** (Ubuntu) launched in the public subnet with a public IP
- **Security Group** allowing inbound SSH (22) and HTTP (80)

## Setup on the EC2 instance

```bash
# 1. Install Docker
sudo apt update && sudo apt install docker.io -y
sudo systemctl enable docker && sudo systemctl start docker
sudo usermod -aG docker $USER   # log out & back in after this

# 2. Clone this repo
git clone https://github.com/Ishachandel1010/three-tier-aws-app.git
cd three-tier-aws-app

# 3. Build and start all three tiers
docker compose up -d --build

# 4. Check everything is running
docker compose ps
```

Visit `http://<your-ec2-public-ip>` in your browser — you'll see the message board app, and messages you add will persist in PostgreSQL.

## Local development

```bash
docker compose up -d --build
```

Then open `http://localhost`.

## Project structure

three-tier-aws-app/
├── app/
│ ├── app.py # Flask application
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # App tier image
│ └── templates/
│ └── index.html # Frontend page
├── nginx/
│ └── nginx.conf # Reverse proxy config
├── screenshots/
│ └── screenshot.png # App screenshot
├── docker-compose.yml # Orchestrates all three tiers
├── .gitignore
└── README.md


## Useful commands

| Command | Purpose |
|---|---|
| `docker compose up -d --build` | Build and start all containers in the background |
| `docker compose ps` | Check container status |
| `docker compose logs -f app` | Tail logs from the app container |
| `docker compose logs -f nginx` | Tail logs from the nginx container |
| `docker compose down` | Stop and remove all containers |
| `docker compose down -v` | Also remove the database volume (wipes data) |

## Tech stack

- **Presentation:** Nginx (reverse proxy)
- **Application:** Python, Flask, Gunicorn
- **Database:** PostgreSQL
- **Orchestration:** Docker & Docker Compose
- **Infrastructure:** AWS EC2 (Ubuntu), custom VPC, subnets, security groups
