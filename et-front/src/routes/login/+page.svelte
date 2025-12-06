<script>
  import { goto } from '$app/navigation';
  import { checkAuth } from '$lib/utils/auth';
  import { onMount } from 'svelte';
  import { PUBLIC_API_URL } from '$env/static/public';

  let username = '';
  let password = '';
  let errorMessage = '';

  async function login(event) {
    event.preventDefault();

    errorMessage = '';

    try {
          const res = await fetch(`${PUBLIC_API_URL}/api/auth/login`, {
              method: 'POST',
              credentials: 'include',          
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  username,
                  password
              })
          });

          if (!res.ok) {
              const data = await res.json();
              errorMessage = data.detail || 'Ошибка входа';
              return;
          } 

          const { role } = await res.json()
          if (role === 'student') {
            goto('/s/mygrades')
          } 
          else if (role === 'teacher') {
            goto('/t/gradebook')
          }
          else if (role === 'admin') {
            goto('/admin/users')
          }

      } catch (e) {
        console.log(e)
        errorMessage = 'Ошибка соединения с сервером';
      }
    }

    onMount(async () => {
        const userData = await checkAuth()
        switch (userData.role) {
            case 'student':
                goto('/s/mygrades');
                break;
            case 'teacher':
                goto('/t/gradebook');
                break;
            case 'admin':
                goto('/admin/users');
                break;
        }
    })
</script>
  
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-4 mt-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Вход</h3>
            
            <form id="loginForm" on:submit={login}>
              <div class="mb-3">
                <label for="email" class="form-label">Имя пользователя</label>
                <input bind:value={username} type="text" class="form-control" id="email" placeholder="Введите имя пользователя" required>
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input bind:value={password} type="password" class="form-control" id="password" placeholder="Введите ваш пароль" required>
              </div>
              
              <button type="submit" class="btn btn-primary w-100">Войти</button>
            </form>

            {#if errorMessage}
            <div id="errorMessage" class="text-danger mt-3 text-center">{errorMessage}</div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>