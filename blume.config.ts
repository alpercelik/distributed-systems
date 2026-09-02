import { defineConfig } from "blume";

export default defineConfig({
  title: "Distributed Systems",
  description:
    "A step-by-step, example-driven course in distributed systems, microservices, and enterprise integration patterns.",
  content: {
    sources: [
      {
        type: "filesystem",
        root: ".",
        include: [
          "README.md",
          "CURRICULUM.md",
          "GLOSSARY.md",
          "spec/**/*.md",
          "domain/**/*.md",
          "modules/**/*.md",
          "reference/**/*.md",
        ],
        exclude: [
          "**/.blume/**",
          "**/.blume-verify/**",
          "**/dist/**",
          "**/node_modules/**",
        ],
      },
    ],
  },
  ai: {
    llmsTxt: true,
  },
  deployment: {
    output: "static",
  },
});
