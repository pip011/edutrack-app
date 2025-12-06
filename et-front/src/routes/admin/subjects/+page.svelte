<script>
    import EditableRow from '$lib/components/EditableRow.svelte';
    import DeleteButton from '$lib/components/DeleteButton.svelte';
    import { invalidate } from '$app/navigation';
    import { fly, fade } from 'svelte/transition';
    import { PUBLIC_API_URL } from '$env/static/public';

    export let data = null;
    let notification = false;
    let isSuccess = true; 
    let successMessage = '';
    let errorMessage = '';
    let selectedSubjectId = null;
    let showAddTeacherForm = false;
    let teacherIdToAdd = '';
    let showCreateSubjectForm = false;
    let subjectNameToAdd = '';

    $: selectedSubjectObject = data
		    ? data.subjects.find(s => String(s.id) === String(selectedSubjectId))
		    : null;

    $: if (selectedSubjectObject) {
        showAddTeacherForm = false;
        teacherIdToAdd = '';
    }

    function showNotification() {
      notification = true;
      setTimeout(() => {
        notification = false;
      }, 3000)
    }

    function handleCreateSubjectForm() {
        showCreateSubjectForm ? showCreateSubjectForm = false : showCreateSubjectForm = true;
        subjectNameToAdd = '';
    }

    function handleRClick(event) {
        selectedSubjectId = event.detail.rowId
    }

    function handleAddTeacherForm() {
        showAddTeacherForm ? showAddTeacherForm = false : showAddTeacherForm = true;
    }

    function handleCancelChoose() {
        selectedSubjectId = null;
    }

    async function handleCreateSubject() {
        let body = {};
      body['name'] = subjectNameToAdd;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/subjects/`, {
            credentials: 'include', 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            let jsonData = await response.json();
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            showNotification()
            return
        }

        await invalidate('app:subjects');
        handleCreateSubjectForm()

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    async function handleDeleteTeacher(event) {
        let body = {};
      body['teacher_id'] = event.detail.id;
      body['subject_id'] = selectedSubjectId;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/subjects/unbind-teacher`, {
            credentials: 'include', 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            let jsonData = await response.json();
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            showNotification()
            return
        }

        await invalidate('app:subjects');

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    async function handleAddTeacherToGroup() {
      let body = {};
      body['teacher_id'] = teacherIdToAdd;
      body['subject_id'] = selectedSubjectId;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/subjects/bind-teacher`, {
            credentials: 'include', 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            let jsonData = await response.json();
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            showNotification()
            return
        }

        await invalidate('app:subjects');

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }
</script>

<div class="d-flex flex-column w-100" style="max-width: 65%">
    <h2 class="mb-4 text-white">Предметы</h2>
    {#if !data}
    <div class='d-flex justify-content-center'>
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
    </div>
    {:else if data.error}
    <p class="text-danger">{data.error}</p>
    {:else}
    {#if selectedSubjectObject != null}
    <h4 class="text-white mb-3">Редактирование предмета <span class="text-warning">"{selectedSubjectObject.name}"</span></h4>
    <h5 class="text-white mb-2">Преподаватели</h5>
    <table class="table table-dark table-hover mb-4 w-50">
      <thead class="table-dark">
        <tr>
          <th>Teacher ID</th>
          <th>Полное имя преподавателя</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
		{#each selectedSubjectObject.teachers as teacher}
        <tr>
            <td>{teacher.id}</td>
            <td>{teacher.full_name}</td>
            <td>
                <div class="d-flex flex-row justify-content-center gap-2">
                    <DeleteButton on:handleDelete={handleDeleteTeacher} id={teacher.id} />
                </div>
            </td>
        </tr>
        {/each}
      </tbody>
    </table>
        {#if showAddTeacherForm}
    <div class="d-flex flex-column gap-1">
      <h6 class="text-white">Введите ID преподавателя</h6>
      <div class="input-group mb-3 w-25">
        <button on:click={handleAddTeacherToGroup} class="btn btn-outline-primary" type="button" id="button-addon1">Добавить</button>
        <input bind:value={teacherIdToAdd} type="number" class="form-control bg-dark text-white border-secondary" placeholder="Введите ID" aria-label="Example text with button addon" aria-describedby="button-addon1">
      </div>
      <button on:click={handleAddTeacherForm} class="btn btn-danger" style="width: 8rem;">Закрыть</button>
    </div>
        {:else}
    <button on:click={handleAddTeacherForm} class="btn btn-success align-self-start">Добавить преподавателя</button>
        {/if}
        <button on:click={handleCancelChoose} class="btn btn-secondary align-self-start mt-4">Назад</button>
    {:else}
    <table class="table table-dark table-hover w-50">
      <thead class="table-dark">
        <tr>
          <th>ID предмета</th>
          <th>Название предмета</th>
        </tr>
      </thead>
      <tbody>
        {#each data.subjects as subject, i}
		    <EditableRow on:handleRowClick={handleRClick} rowId={subject.id} items={[subject.id, subject.name]} />
		{/each}
      </tbody>
    </table>
    <h4 class="text-white mb-3">Действия</h4>
    {#if showCreateSubjectForm}
    <div class="d-flex flex-column p-1">
        <h5 class="mb-3 text-white">Создать предмет</h5>
        <h6 class="mb-1 text-white">Название предмета</h6>
        <form on:submit|preventDefault={handleCreateSubject}>
        <div class="input-group mb-2 w-25">
          <input bind:value={subjectNameToAdd} required type="text" class="form-control bg-dark text-white border-secondary mb-2 w-50" placeholder="Введите название">
        </div>
        <div class="d-flex flex-row gap-2">
          <button type="submit" class="btn btn-primary align-self-start">Создать</button>
          <button on:click={handleCreateSubjectForm} class="btn btn-secondary align-self-start">Вернуться</button>
        </div>
        </form>
    </div>
    {:else}
    <button on:click={handleCreateSubjectForm} class="btn btn-success align-self-start">Создать предмет</button>
    {/if}
    {/if}
    {/if}

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
</div>