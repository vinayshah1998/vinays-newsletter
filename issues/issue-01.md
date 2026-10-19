# Bookmark Digest, Issue #1: Push to Main, Ask Questions Later
*Oct 12 – Oct 17, 2026 (PT) · 20 bookmarks, curated*

Welcome to the first issue. You saved a week of agent harnesses, arguments about pull requests, and one Carl Jung quote.
No turntables this time, so the receiver can keep idling. Let's go.

---

## Agent harnesses and runtimes

### [Harness²: recursive agent harnessing, from Google Research](https://x.com/hmsk/status/2111319218692280472)
**hmsk (@hmsk)** · *GitHub repo + paper*

hmsk links google-research/harness2 with a dry note in Japanese that roughly says "pretty much everyone is building their own version of this." Per the README, Harness² tunes the *harness* (system prompt, guardrails, memory, tool guidance, subagents, skills, scripts, plugins) while leaving model weights alone. It runs a "Propose–Probe–Compose" loop and reports gains of up to 11.5 points on WorkBuddy-Bench, with OpenCode and Codex executors supported.

**Why it matters:** This is basically A/B testing for agent scaffolding: try edits, compare the runs, keep the winner. It reads like WebLab and your coding-agent product had a research paper together.

### [Build with Pi Durable on Cloudflare](https://x.com/pidotdev/status/2111100406612861105)
**Pi (@pidotdev)** · *tutorial blog post*

A walkthrough of a multiplayer chat agent where each session lives in its own Durable Object. It covers hibernation, scheduled tasks mapped onto the object's single alarm, conversation forks, and a durable `search_history` subagent that can be replayed safely if it's evicted mid-call.

**Why it matters:** Long-running agents that sleep until there's work are a real cost problem, and the idempotency tricks here (request-ID receipts, rebuilding the alarm on every wake) carry over to any agent backend.

### [Radius: inference built for Pi](https://x.com/earendilworks/status/2110438891928826351)
**Earendil (@earendilworks)** · *product launch*

Radius is an early-alpha hosted service from the team behind Pi: an AI gateway with org-level controls and analytics, artifact sharing, and web search, all managed through a Radius MCP server.

**Why it matters:** It shows the "harness company also sells the gateway" playbook. Worth watching if your team is weighing build vs. buy for agent infrastructure.

### [skin: an app that rewrites itself and can't brick itself](https://x.com/acoyfellow/status/2111286813776023583)
**Jordan Coeyman (@acoyfellow)** · *demo app*

A Pi Durable agent lives inside your own copy of a web app. Every change it makes gets bundled into a Durable Object, booted in a Worker Loader isolate, and checked, and it only goes live if it passes. If something crashes in the browser, it rolls back automatically. Model calls run on *your* Cloudflare account.

**Why it matters:** "Self-modifying app" sounds scary until a gate stands between the agent and production. That's the same idea as safe deployment, just very small.

---

## Building agent products

### [38 lessons from building 10 AI products at PostHog](https://x.com/posthog/status/2109706421919248499)
**PostHog (@posthog)** · *long thread*

PostHog's AI products have nearly 100k monthly users, and this thread collects what they learned. From the part I read (lessons 19–38): many agent failures are context failures, subagents cost more than you think because they don't share the parent's cache, their wizard costs $6.67 a run, and "a missing tool is a feature request written by a robot."

**Why it matters:** Lesson 34 (read traces, write a small eval, improve against it) is the experimentation loop you already know, applied to agents. Lesson 38 is a good reminder: "expect half these things to be wrong in a year."

### [How do you trust your agents' work more?](https://x.com/poteto/status/2111133080526495985)
**lauren (@poteto)** · *thread + plugin (pstack)*

An inverted pyramid of trust: put most of the effort into codebase improvements, then static analysis, then prose (AGENTS.md, skills), and save human review for last. She points to **pstack**, a Cursor/Claude Code plugin whose `/poteto-mode` routes work through 23 playbooks (bug fix, perf, hillclimb, forensics…).

**Why it matters:** "Make the easy thing the right thing" is a good design rule for a coding-agent product, and the pstack playbooks are worth borrowing from.

### [What a software factory really is](https://x.com/zachlloydtweets/status/2111165023238160603)
**Zach Lloyd (@zachlloydtweets)** · *recorded talk (video)*

The Warp founder re-recorded his AI Engineer NYC talk for X. His tl;dr: software engineering is turning into factory engineering, and engineers should start on new work like factory benchmarking. (The video is on X, so I only had the post text.)

**Why it matters:** "Factory benchmarking" is close to measuring agent throughput and quality at scale, which is right where you work.

### [What agents mean for Rust (and vice versa)](https://x.com/badlogicgames/status/2110308164776100275)
**Mario Zechner (@badlogicgames)** · *blog post recommendation*

Mario recommends a post on the *baby steps* blog. The author, a longtime programming-language designer, argues that Rust's "if it compiles, it works" guardrails suit agents well, that tests alone aren't enough, and that Rust should aim for proof tools that can show unsafe code is sound. There's also a cameo from Amazon's #aws-memes Slack channel.

**Why it matters:** It makes a clear case that type systems and verifiers are what keep agents on track. Also good context for any language choices your agent makes.

### [Constrained Decoding Models (CDMs)](https://x.com/neal_k_patel/status/2109978626124898587)
**Neal Patel (@neal_k_patel)** · *model launch (video)*

The scaledown CEO announces single-task models for classify, extract, and summarize that skip the token-by-token generation loop. The post claims 1M-token multimodal input, $0.05/M input tokens with free output, and "200x faster, 467x cheaper than frontier LLM APIs."

**Why it matters:** Those are vendor claims, so be skeptical, but routing and context compaction are real needs inside a coding agent, and a cheap classifier is a natural fit for both.

---

## Review, CI, and shipping

### [Why are you still using pull requests?](https://x.com/thorstenball/status/2111130129355481240)
**Thorsten Ball (@thorstenball)** · *opinion thread*

The Amp engineer argues that agents can review code, explain it, and run the full test suite before pushing, so PRs mostly slow you down. Continuous integration originally meant the *opposite* of long-lived branches anyway.

**Why it matters:** Whether you agree or not, this is the argument your users will make once the agent is the one writing most of the diffs.

### [How Amp actually pushes to main](https://x.com/thorstenball/status/2111115720637722945)
**Thorsten Ball (@thorstenball)** · *process breakdown*

The details: Buildkite runs tests, GitHub Actions runs security checks and deploys (staging, then prod, usually in about 10 minutes), a failed check blocks deploy and pings the author in Slack, and CLI releases go out every 4 hours. It quotes his earlier post linking Amp's ["That's not SOC 2 compliant" note](https://ampcode.com/notes/thats-not-soc-2-compliant), which says SOC 2 asks for authorized, tested, approved, recorded changes, not specifically PRs.

**Why it matters:** This is the concrete version of the thread above, and the SOC 2 note is useful the next time someone says "compliance won't allow it."

### [Build your own agentic code reviewer](https://x.com/CraigBarrDev/status/2111250498733175150)
**Craig B. (@CraigBarrDev)** · *opinion thread*

Quoting Boris Cherny's praise for Claude Code Review, Craig argues for a reviewer you build yourself: trigger it with a GitHub webhook, give it architecture context and risk guidelines, separate nits from blockers, and let it request changes so coding agents have to fix the risks. His warning: "A nit picking agentic code review can be worse than not having one at all."

**Why it matters:** It's a clear blueprint for risk-tiered automated review, a feature your product might ship or need to work alongside.

### [Run recurring jobs on Stripe without a cron server](https://x.com/Hi_Mrinal/status/2110544804765696364)
**Mrinal (@Hi_Mrinal)** · *engineering blog post*

Stripe Workflows now has recurring schedule triggers that follow local time, including DST. The example is a weekday past-due-subscription check that writes its "already notified" state into metadata keyed by invoice ID, so it alerts once per invoice.

**Why it matters:** The cron-vs-DST problem and the idempotency trick are good tips for your own scheduled jobs, homelab ones included.

---

## Claude Code field notes

### [Claude Code now gzips every turn](https://x.com/ClaudeDevs/status/2111209208012210409)
**ClaudeDevs (@ClaudeDevs)** · *product update*

Claude Code now compresses the conversation it sends each turn so it reaches the model faster, and cloud sessions start up as soon as you start typing.

**Why it matters:** It's a cheap latency fix that any coding agent sending large contexts every turn could copy.

### […and someone points out zstd exists](https://x.com/soft_fox_lad/status/2111462268881801263)
**fox (@soft_fox_lad)** · *quote-post*

Quoting the gzip news: "You can join any company and improve their software 100 fold by telling them that avif/jpeg xl/zstd/brotli are things that exist."

**Why it matters:** If you add compression to your agent's payloads, benchmark zstd and brotli before you pick gzip.

### [Idle compaction in Claude Code](https://x.com/lydiahallie/status/2110484840256819380)
**Lydia Hallie (@lydiahallie)** · *feature announcement*

Long idle sessions now get compacted right before the prompt cache expires (about 1h), so when you return the model reprocesses only the summary instead of the whole conversation.

**Why it matters:** Timing compaction to the cache expiry is a clever cost trick, and you can apply the same idea to session management in your product.

---

## Off the main branch

### [Anthropic Fellows Program: January cohort](https://x.com/suraj_sharma14/status/2110377588975943987)
**Suraj Sharma (@suraj_sharma14)** · *opportunity post*

Anthropic's page lists a 4-month funded AI safety research fellowship with about $15K/month in compute and mentorship, open to people without a PhD or prior ML experience. The post cites a $3,850/week stipend.

**Why it matters:** The January cohort deadline is **Oct 18**, which is today, so it's now or the next cohort.

### [Advice that only 2 applicants took](https://x.com/chrislevan24/status/2110756150677529062)
**chris (@chrislevan24)** · *quote-post*

Someone on the growth team at @trynationgraph says only about 2 of hundreds of applicants for their growth engineer role took his advice. The advice is in his X Article "how to win the startup interview process [full guide]," but X reports the article link as 404, so I couldn't read it.

**Why it matters:** Hiring and mentoring material, if the article ever loads. Mostly it's a reminder that following instructions is rare enough to stand out.

### [Shop your loan at local banks first](https://x.com/Nickeubanks/status/2110181587883336112)
**nick Ξubanks (@Nickeubanks)** · *quote-post*

He calls Amanda Orson's tip "S Tier advice": use iBankNet's bank map to list the banks in your state by assets, then call local banks, where your loan matters more than it would at a megabank.

**Why it matters:** It's practical money advice for the day a mortgage or a small-business loan comes up.

### [Carl Jung, 1944](https://x.com/readswithravi/status/2110210988892942396)
**Reads with Ravi (@readswithravi)** · *quote*

"People will do anything, no matter how absurd, to avoid facing their own souls…"

**Why it matters:** It's a nice change of pace in a week of harness diagrams. Also, "they cannot get on with themselves" fits every agent stuck in a retry loop.

---

## Pick of the week
**[Harness²](https://x.com/hmsk/status/2111319218692280472).** You spent five years on WebLab and now build a coding agent, and here's a Google Research framework that treats the agent harness as something you optimize by running contrasting experiments, with benchmarks to back it up. Read the README, then try `harness2-demo`. It runs locally with no model credentials.

*Bookmark Digest · built from your latest 20 bookmarks · see you Saturday.*
