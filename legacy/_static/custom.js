// Javascript from ChatGPT to insert a class into the <body> tag
document.addEventListener("DOMContentLoaded", () => {
  // grab the page filename without extension
  const slug = window.location.pathname.split("/").pop().split(".")[0];
  if (slug.startsWith("AAA")) {
    document.body.classList.add("aaa-page");
  }
});