<script>
  import { PUBLIC_API_URL } from '$env/static/public';
  import { goto } from '$app/navigation';

  async function logout() {
    await fetch(`${PUBLIC_API_URL}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    });
    goto('/login');
  }
</script>
<button on:click={logout} class="btn btn-danger mt-auto" style="align-self: self-start;">Выход</button>