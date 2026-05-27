"use client";

import { FormEvent, useState } from "react";

type Preview = {
  url: string;
  platform: string;
  title: string | null;
  description: string | null;
  image: string | null;
  author: string | null;
  author_url: string | null;
  embed_html: string | null;
  video_url: string | null;
  thumbnail_url: string | null;
};

export default function Home() {
  const [targetUrl, setTargetUrl] = useState("");
  const [preview, setPreview] = useState<Preview | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedUrl = targetUrl.trim();
    if (!trimmedUrl) {
      setError("Veuillez saisir une URL.");
      setStatus("error");
      return;
    }

    setStatus("loading");
    setError(null);
    setPreview(null);

    try {
      const response = await fetch(`/api/preview?url=${encodeURIComponent(trimmedUrl)}`, {
        cache: "no-store",
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Erreur lors de la récupération du preview.");
      }

      setPreview(data);
      setStatus("success");
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Erreur inconnue.");
      setStatus("error");
    }
  }

  return (
    <div className="min-h-screen bg-zinc-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <main className="mx-auto flex min-h-screen w-full max-w-4xl flex-col gap-8 px-6 py-10">
        <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h1 className="text-3xl font-semibold">LinkPeek</h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600 dark:text-slate-400">
            Entrez une URL Facebook, Instagram ou TikTok et récupérez un aperçu propre depuis le backend.
          </p>

          <form onSubmit={handleSubmit} className="mt-8 flex flex-col gap-4 sm:flex-row">
            <label className="sr-only" htmlFor="preview-url">
              URL à prévisualiser
            </label>
            <input
              id="preview-url"
              type="url"
              value={targetUrl}
              onChange={(event) => setTargetUrl(event.target.value)}
              placeholder="https://..."
              className="min-w-0 flex-1 rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
            />
            <button
              type="submit"
              className="inline-flex items-center justify-center rounded-2xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-950 dark:hover:bg-slate-200"
            >
              {status === "loading" ? "Chargement..." : "Récupérer"}
            </button>
          </form>

          {status === "error" && error ? (
            <div className="mt-4 rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-700 dark:bg-red-950/40 dark:text-red-200">
              {error}
            </div>
          ) : null}
        </section>

        {preview ? (
          <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
                  Aperçu {preview.platform}
                </p>
                <h2 className="mt-2 text-2xl font-semibold text-slate-950 dark:text-slate-100">
                  {preview.title || "Aucune titre disponible"}
                </h2>
              </div>
              <a
                href={preview.url}
                target="_blank"
                rel="noreferrer"
                className="rounded-full border border-slate-300 px-4 py-2 text-sm text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
              >
                Ouvrir la source
              </a>
            </div>

            <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_280px]">
              <div className="space-y-4">
                {preview.description ? (
                  <p className="text-sm leading-7 text-slate-600 dark:text-slate-300">
                    {preview.description}
                  </p>
                ) : null}

                <div className="grid gap-3 sm:grid-cols-2">
                  {preview.author ? (
                    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950/60">
                      <p className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Auteur</p>
                      <p className="mt-2 text-sm font-medium text-slate-900 dark:text-slate-100">
                        {preview.author}
                      </p>
                      {preview.author_url ? (
                        <a
                          href={preview.author_url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-1 block text-xs text-slate-600 underline dark:text-slate-400"
                        >
                          Profil auteur
                        </a>
                      ) : null}
                    </div>
                  ) : null}

                  {preview.video_url ? (
                    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950/60">
                      <p className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Vidéo</p>
                      <a
                        href={preview.video_url}
                        target="_blank"
                        rel="noreferrer"
                        className="mt-2 block text-sm font-medium text-slate-900 underline dark:text-slate-100"
                      >
                        Ouvrir la vidéo
                      </a>
                    </div>
                  ) : null}
                </div>

                {preview.embed_html ? (
                  <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950/60">
                    <p className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Embed HTML</p>
                    <div
                      className="mt-3 text-sm leading-6 text-slate-700 dark:text-slate-300"
                      dangerouslySetInnerHTML={{ __html: preview.embed_html }}
                    />
                  </div>
                ) : null}
              </div>

              <div className="space-y-4">
                {preview.image ? (
                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950/60">
                    <img src={preview.image} alt={preview.title ?? "Preview image"} className="h-full w-full object-cover" />
                  </div>
                ) : null}

                {preview.thumbnail_url ? (
                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950/60">
                    <img src={preview.thumbnail_url} alt="Thumbnail" className="h-full w-full object-cover" />
                  </div>
                ) : null}
              </div>
            </div>
          </section>
        ) : status === "idle" ? (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-slate-600 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400">
            Entrez une URL pour voir le preview du backend.
          </section>
        ) : null}
      </main>
    </div>
  );
}
