<script>
    import { fly, fade } from 'svelte/transition';
    import { goto, invalidate } from '$app/navigation';
    import { PUBLIC_API_URL } from '$env/static/public';

    import DeleteButton from '$lib/components/DeleteButton.svelte';
    import EditableUserCell from "$lib/components/EditableUserCell.svelte";

    export let data = null;
    let notification = false;
    let isSuccess = true;
    let successMessage = 'Операция выполнена успешно.'
    let errorMessage = 'Операция выполнена безуспешно.'
    let usernameToCreateUser = '';
    let passwordToCreateUser = '';
    let roleToCreateUser = 'student';
    let showCreateUserForm = false;

    function showNotification() {
      notification = true;
      setTimeout(() => {
        notification = false;
      }, 3000)
    }

    function handleCreateUserForm() {
      showCreateUserForm ? showCreateUserForm = false : showCreateUserForm = true
      passwordToCreateUser = '';
      roleToCreateUser = 'student';
    }

    async function handleCreateUser() {
      let body = {};
      body['username'] = usernameToCreateUser;
      body['password'] = passwordToCreateUser;
      body['role'] = roleToCreateUser;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/auth/register`, {
            credentials: 'include', 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + response.detail
            showNotification()
            return
        }

        await await invalidate('app:users');

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    async function handleDeleteUser(event) {
      let userId = event.detail.id;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/users/delete/${userId}`, {
            credentials: 'include', 
            method: 'POST'
        });

        if (!response.ok) {
            isSuccess = false;
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + response.statusText
            showNotification()
            return
        }

        await invalidate('app:users');

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    function onUpdateHandler() {
      isSuccess = true;
      successMessage = 'Операция выполнена успешно.'
      showNotification()
    }
</script>

<div class="d-flex flex-column" style="max-width: 65%">
    <h2 class="mb-4 text-white">Список пользователей</h2>
    {#if !data}
    <div class='d-flex justify-content-center'>
      <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
    </div>
    {:else if data.error}
    <p class="text-danger">{data.error}</p>
    {:else}
    <table class="table table-dark table-striped">
        <thead class="table-dark">
          <tr>
            <th>User ID</th>
            <th>Роль</th>
            <th>Username</th>
            <th>Student ID</th>
            <th>Teacher ID</th>
            <th>Полное имя</th>
            <th>Дата рождения</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {#each data.users as user}
            <tr>
              <td>{user.id}</td>
              <td>{user.role}</td>
              <td>{user.username}</td>
            {#if user.teacher}
              <td>-</td>
              <td>{user.teacher.id}</td>
              <td><EditableUserCell on:update={onUpdateHandler} value={user.teacher.full_name} field='full_name' entity='teacher' userId={user.id} /></td>
              <td><EditableUserCell on:update={onUpdateHandler} value={user.teacher.birth_date} field='birth_date' entity='teacher' userId={user.id} isBirthDate=true /></td>
            {:else if user.student}
              <td>{user.student.id}</td>
              <td>-</td>
              <td><EditableUserCell on:update={onUpdateHandler} value={user.student.full_name} field='full_name' entity='student' userId={user.id} /></td>
              <td><EditableUserCell on:update={onUpdateHandler} value={user.student.birth_date} field='birth_date' entity='student' userId={user.id} isBirthDate=true /></td>
            {:else}
              <td>-</td>
              <td>-</td>
              <td>-</td>
              <td>-</td>
            {/if}
            <td>
              <div class="d-flex flex-row justify-content-center gap-2">
                <DeleteButton on:handleDelete={handleDeleteUser} id={user.id} />
              </div>
            </td>
            </tr>
          {/each}
        </tbody>
    </table>
    {/if}
    <div class="d-flex flex-column gap-2">
<h4 class="text-white">Действия</h4>
{#if showCreateUserForm}
<div class="d-flex flex-column p-1">
    <h5 class="mb-3 text-white">Создать пользователя</h5>
    <form on:submit|preventDefault={handleCreateUser}>
      <h6 class="mb-1 text-white">Имя пользователя</h6>
    <div class="input-group mb-2 w-25">
      <input bind:value={usernameToCreateUser} minlength="6" type="text" class="form-control bg-dark text-white border-secondary mb-2">
    </div>
    <h6 class="mb-1 text-white">Пароль</h6>
    <div class="input-group mb-4 w-25">
      <input bind:value={passwordToCreateUser} minlength="6" type="text" class="form-control bg-dark text-white border-secondary">
    </div>
    <h6 class="mb-1 text-white">Роль</h6>
    <div class="d-flex flex-row gap-2">
      <div class="form-check mb-4">
      <input
        type="radio"
        id="rolestudent"
        name="role"
        value="student"
        bind:group={roleToCreateUser}
        class="form-check-input"
      >
      <label for="rolestudent" class="form-check-label text-white">Студент</label>
    </div>

    <div class="form-check mb-4">
      <input
        type="radio"
        id="roleteacher"
        name="role"
        value="teacher"
        bind:group={roleToCreateUser}
        class="form-check-input"
        checked
      >
      <label for="roleteacher" class="form-check-label text-white">Преподаватель</label>
    </div>
    </div>

    <div class="d-flex flex-row gap-2">
      <button type="submit" class="btn btn-primary align-self-start">Создать</button>
      <button on:click={handleCreateUserForm} class="btn btn-secondary align-self-start">Вернуться</button>
    </div>
    </form>
    
</div>
{:else}
<button on:click={handleCreateUserForm} class="btn btn-success align-self-start">Создать пользователя</button>
{/if}
</div>
</div>


{#if notification}
<div 
  class={isSuccess ? "alert alert-success" : "alert alert-danger"}
  role="alert"
  style="
    width: auto;
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1050;
    min-width: 200px;
  "
  in:fly={{ x: 100, duration: 300 }}
  out:fly={{ x: 100, duration: 300 }}
>
  {isSuccess ? successMessage : errorMessage}
</div>
{/if}