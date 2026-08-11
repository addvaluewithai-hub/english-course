const ROOT = new URL("../../../", import.meta.url);

async function json(path) {
  const response = await fetch(new URL(path, ROOT));
  if (!response.ok) throw new Error(`تعذر تحميل ${path}`);
  return response.json();
}

async function text(path) {
  const response = await fetch(new URL(path, ROOT));
  if (!response.ok) throw new Error(`تعذر تحميل ${path}`);
  return response.text();
}

export function loadRelease() {
  return json("data/reviewed/a1-first-10-lessons-pilot-v1.json");
}

export function loadScope() {
  return json("data/reviewed/a1-scope-and-sequence-v1.json");
}

export async function loadLesson(contract) {
  const base = `${contract.content_path}/`;
  const [manifest, content, activities, assessment, packet, transcript, scene, context] =
    await Promise.all([
      json(`${base}lesson-manifest.json`),
      json(`${base}content.json`),
      json(`${base}activities.json`),
      json(`${base}assessment.json`),
      json(`${base}source-packet.json`),
      text(`${base}video/transcript.txt`),
      text(`${base}video/scene.txt`),
      text(`${base}video/sample-context.txt`),
    ]);
  return { contract, manifest, content, activities, assessment, packet, transcript, scene, context };
}
