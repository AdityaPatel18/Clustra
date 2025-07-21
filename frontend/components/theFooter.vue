<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; {{ new Date().getFullYear() }} Clustra. All rights reserved.</p>
      <div class="footer-links">
        <!-- <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
        <a href="/contact">Contact</a> -->
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #f2f2f2;
  padding: 1.5rem 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  border-top: 1px solid #ddd;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-links {
  margin-top: 0.5rem;
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.footer-links a {
  color: #555;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #222;
}
</style>