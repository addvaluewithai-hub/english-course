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

async function optionalVideo(lessonId) {
  const url = new URL(`../media/${lessonId}.mp4`, import.meta.url);
  try {
    const response = await fetch(url, { method: "HEAD" });
    return response.ok ? url.href : null;
  } catch {
    return null;
  }
}

export async function loadLesson(contract) {
  const base = `${contract.content_path}/`;
  const [manifest, content, activities, assessment, packet, transcript, scene, context, videoUrl] =
    await Promise.all([
      json(`${base}lesson-manifest.json`),
      json(`${base}content.json`),
      json(`${base}activities.json`),
      json(`${base}assessment.json`),
      json(`${base}source-packet.json`),
      text(`${base}video/transcript.txt`),
      text(`${base}video/scene.txt`),
      text(`${base}video/sample-context.txt`),
      optionalVideo(contract.lesson_id),
    ]);
  return { contract, manifest, content, activities, assessment, packet, transcript, scene, context, videoUrl };
}
