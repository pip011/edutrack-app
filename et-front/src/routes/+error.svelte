<script>
    import { goto } from '$app/navigation'

    export let status = 404;
    export let message = "Страница не найдена";
</script>

<div class="container vh-100 d-flex flex-column justify-content-center align-items-center text-center">
  <div class="card shadow-sm p-5">
    <h1 class="display-1 text-danger">{status}</h1>
    <h3 class="mb-3">{message}</h3>
  </div>
</div>