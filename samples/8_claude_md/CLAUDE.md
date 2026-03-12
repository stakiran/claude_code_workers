# MyProject

## Quick Start
- `npm install` - Install dependencies
- `npm run dev` - Start dev server (localhost:3000)
- `npm test` - Run test suite
- `npm run build` - Production build

## Tech Stack
- TypeScript + Next.js 14
- PostgreSQL + Prisma ORM
- Jest for testing

## Code Style
- 2-space indentation
- Trailing commas in multiline
- Always include return type annotations
- Max line length: 100

## API Conventions
- RESTful endpoints under `/api/v1/`
- Error format: `{ error: string, code: string }`
- All POST/PUT/PATCH require request validation

## Git Workflow
- Branch naming: `feature/xxx`, `fix/xxx`
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Require PR review before merge to main

## References
See @docs/architecture.md for system design
See @docs/database.md for schema documentation
