import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";

import { decodeBrief } from "../../src/api/client";
import type { DecodeRunResponse } from "../../src/api/types";
import "./style.css";

type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "succeeded"; run: DecodeRunResponse }
  | { status: "failed"; message: string; run?: DecodeRunResponse };

function Popup(): React.ReactElement {
  const [text, setText] = useState("");
  const [requestState, setRequestState] = useState<RequestState>({ status: "idle" });
  const [copyState, setCopyState] = useState<"idle" | "copied" | "failed">("idle");

  const canSubmit = text.trim().length > 0 && requestState.status !== "loading";
  const resultJson = useMemo(() => {
    if (requestState.status !== "succeeded" && requestState.status !== "failed") {
      return "";
    }
    if (!requestState.run?.structured_result) {
      return "";
    }
    return JSON.stringify(requestState.run.structured_result, null, 2);
  }, [requestState]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    if (!canSubmit) {
      return;
    }

    setCopyState("idle");
    setRequestState({ status: "loading" });

    try {
      const run = await decodeBrief(text.trim());
      if (run.status === "succeeded") {
        setRequestState({ status: "succeeded", run });
        return;
      }
      setRequestState({
        status: "failed",
        message: run.safe_error_message ?? "Brief decoding failed.",
        run,
      });
    } catch (error) {
      setRequestState({
        status: "failed",
        message: error instanceof Error ? error.message : "Brief decoding failed.",
      });
    }
  }

  async function handleCopy(): Promise<void> {
    if (!resultJson) {
      return;
    }

    try {
      await navigator.clipboard.writeText(resultJson);
      setCopyState("copied");
    } catch {
      setCopyState("failed");
    }
  }

  return (
    <main className="popup-shell">
      <header className="header">
        <h1>AI Brief Decoder Lite</h1>
        <p>Turn messy task text into a structured brief.</p>
      </header>

      <form className="form" onSubmit={handleSubmit}>
        <label htmlFor="brief-text">Brief text</label>
        <textarea
          id="brief-text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Paste a task, project brief, or rough request..."
          rows={7}
        />
        <button type="submit" disabled={!canSubmit}>
          {requestState.status === "loading" ? "Decoding..." : "Run decode"}
        </button>
      </form>

      {requestState.status === "loading" ? <p className="notice">Working...</p> : null}

      {requestState.status === "failed" ? (
        <section className="error" role="alert">
          <strong>Error</strong>
          <p>{requestState.message}</p>
        </section>
      ) : null}

      {(requestState.status === "succeeded" || requestState.status === "failed") &&
      requestState.run?.structured_result ? (
        <ResultView
          run={requestState.run}
          copyState={copyState}
          onCopy={() => {
            void handleCopy();
          }}
        />
      ) : null}
    </main>
  );
}

interface ResultViewProps {
  run: DecodeRunResponse;
  copyState: "idle" | "copied" | "failed";
  onCopy: () => void;
}

function ResultView({ run, copyState, onCopy }: ResultViewProps): React.ReactElement | null {
  const result = run.structured_result;
  if (!result) {
    return null;
  }

  return (
    <section className="result">
      <div className="result-heading">
        <h2>Result</h2>
        <button type="button" className="secondary" onClick={onCopy}>
          {copyState === "copied" ? "Copied" : "Copy JSON"}
        </button>
      </div>
      {copyState === "failed" ? <p className="copy-error">Clipboard write failed.</p> : null}

      <Article title="Summary">
        <p>{result.summary}</p>
      </Article>
      <ListArticle title="Goals" items={result.goals} />
      <ListArticle title="Deliverables" items={result.deliverables} />
      <ListArticle title="Constraints" items={result.constraints} />

      <Article title="Risks">
        <ul className="risk-list">
          {result.risks.map((risk) => (
            <li key={`${risk.risk}-${risk.severity}`}>
              <span className={`severity severity-${risk.severity}`}>{risk.severity}</span>
              <span>{risk.risk}</span>
              <small>{risk.reason}</small>
            </li>
          ))}
        </ul>
      </Article>

      <ListArticle title="Questions" items={result.clarifying_questions} />
      <Article title="Recommended next action">
        <p>{result.recommended_next_action}</p>
      </Article>
    </section>
  );
}

interface ArticleProps {
  title: string;
  children: React.ReactNode;
}

function Article({ title, children }: ArticleProps): React.ReactElement {
  return (
    <article className="section">
      <h3>{title}</h3>
      {children}
    </article>
  );
}

interface ListArticleProps {
  title: string;
  items: string[];
}

function ListArticle({ title, items }: ListArticleProps): React.ReactElement {
  return (
    <Article title={title}>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">None.</p>
      )}
    </Article>
  );
}

const root = document.getElementById("root");

if (root === null) {
  throw new Error("Popup root element was not found.");
}

createRoot(root).render(
  <React.StrictMode>
    <Popup />
  </React.StrictMode>,
);
