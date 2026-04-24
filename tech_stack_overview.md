# Review Analytics Platform: Technical Architecture & Design Decisions

This document outlines the core technologies and architectural decisions that power the Review Analytics Platform. The stack was deliberately chosen to provide a blend of rapid prototyping speed, embedded Machine Learning capabilities, and a seamless developer experience.

---

## 1. Core Framework: Next.js (App Router) & React
**How it's used:** Next.js serves as the backbone for both the visual Frontend (Customer and Seller portals) and the underlying API routes (`/api/reviews`, `/api/analytics`, etc.).
**Why it was chosen:** 
- **Full-Stack Capabilities:** Using Next.js allowed us to build robust Backend controllers directly alongside the UI code, preventing the need to spin up and maintain a wholly separate Express.js server.
- **App Router Integration:** We utilized the modern `app/` directory structure for fast native routing, layout management, and Server-Side Rendering (SSR) potential.

## 2. Database Layer: Prisma ORM & SQLite
**How it's used:** Prisma is utilized as the database driver natively parsing a `schema.prisma` file, which defines our `Seller`, `Product`, and `Review` models. The actual database relies on a local SQLite file (`dev.db`).
**Why it was chosen:**
- **Zero-Friction Prototyping:** SQLite operates as a single file on your local machine. It requires zero cloud configuration, zero docker containers, and zero database server installation, making it the absolute best tool for local development.
- **Type-Safety:** Prisma automatically generates highly strict TypeScript types for all database queries, catching syntax errors during compilation rather than in production.

## 3. Local Machine Learning: `@xenova/transformers.js`
**How it's used:** Buried inside `src/utils/sentimentAnalyzer.ts`, we embedded a miniaturized, JavaScript-compatible version of HuggingFace's `DistilBERT` model fine-tuned on the SST-2 dataset.
**Why it was chosen:**
- **Cost & Speed:** Instead of charging you for external OpenAI API tokens to analyze every single review, or forcing you to maintain a bulky Python backend, `Transformers.js` allows heavy Machine Learning inference to happen *natively* inside the Node.js process with zero external API calls. It's completely free, offline, and instantaneous. 

## 4. Analytical Tracking: Aspect-Based Sentiment Analysis (ABSA)
**How it's used:** We built a custom NLP pipeline (`absaPipeline.ts`) that extracts specific product "Aspects" (like *Battery*, *Delivery*, *Camera*) from a review string using a sliding-context window. It then runs our localized ML model exclusively over that small chunk of text.
**Why it was chosen:**
- Traditional sentiment analysis just tells you a review is "Negative." Our ABSA approach allows the Dashboard to pinpoint *exactly why* it is negative, giving you actionable AI Recommendations like "Multiple users cited issues with battery life" rather than just showing a massive negative volume.

## 5. UI/UX & Data Visualization: TailwindCSS & Recharts
**How it's used:** `TailwindCSS` provides all layout, typography, and color styling directly via utility classes. `Recharts` mathematically binds server data to the visual charts (Pie, Bar, Line).
**Why it was chosen:**
- **Tailwind:** Enabled the platform's distinct "modern glassmorphism" aesthetic (deep space blue/purple gradients with frosted glass borders) without needing to write a single massive `.css` stylesheet. 
- **Recharts:** Built natively for React on top of D3. It handles all the complex SVG rendering logic required to make the dashboard's "Overall Sentiment" and "Weekly Trends" charts beautifully responsive and hover-interactive.

## 6. Authentication: JWT & Bcrypt
**How it's used:** Seller passwords are mathematically hashed using `bcrypt` before hitting the database. When a seller logs in, the Server signs a cryptographic JSON Web Token (JWT) and places it into an HTTP-only browser cookie.
**Why it was chosen:**
- This is the industry-standard methodology for secure, stateless authentication. By securely wrapping the session in an `httpOnly` cookie, the seller portal is fundamentally protected against malicious client-side JavaScript tampering (XSS).

## 7. Python Fallback Scripts (Backend Prototyping)
**How it's used:** You'll notice artifacts like `backend/app/ai_pipeline.py` and `test_vader.py` relying on libraries like `FastAPI` and `vaderSentiment`.
**Why it was chosen:**
- Python remains the gold standard for exploratory Data Science. Initially, experimental scripts were written here to test Sarcasm logic and Fake Review detection speeds before porting the most efficient algorithms natively back into the Next.js platform for a unified stack.
