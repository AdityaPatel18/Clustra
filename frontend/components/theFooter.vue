<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; {{ new Date().getFullYear() }} Clustra. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #2e1503;
  padding: 1.5rem 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: #f5f5dc;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
