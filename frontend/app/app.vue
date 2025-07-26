<template>
  <NuxtPage />
</template>

<script setup>
onMounted(() => {
  history.pushState(null, "", location.href);
  window.addEventListener("popstate", () => {
    history.pushState(null, "", location.href);
  });

  const navEntry = performance.getEntriesByType("navigation")[0];
  if (navEntry?.type === "reload") {
    window.location.href = "/";
  }
});
</script>
