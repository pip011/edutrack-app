import { PUBLIC_API_URL } from "$env/static/public";

export async function getIdForTeacher() {
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/users/teachers`, {
            credentials: 'include'
        });

        if (!response.ok) {
            let jsonData = await response.json();
            let errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            return { error: errorMessage }
        }

        const data = await response.json();
        return data;

    } catch (e) {
        return { error: e.message };
    }
}

export async function loadSubjectsForTeacher(teacher_id) {
    let body = {};
    body['id'] = teacher_id;

    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/subjects/without-teachers`, {
            credentials: 'include', 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            let jsonData = await response.json();
            let errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            return { error: errorMessage }
        }

        const json = await response.json();
        return json.subjects;

    } catch (e) {
        return { error: e.message };
    }
}

export async function loadGroups() {
    let body = {};

    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups`, {
            credentials: 'include'
        });

        if (!response.ok) {
            let jsonData = await response.json();
            let errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            return { error: errorMessage }
        }

        const json = await response.json();
        return json.groups;

    } catch (e) {
        return { error: e.message };
    }
}

export async function loadGradesBySubjectWithYearAndMonth(subject_id, month, year) {
    let body = {};
    body['subject_id'] = subject_id;
    body['month'] = month;
    body['year'] = year;

    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/grades/sorted`, {
            credentials: 'include', 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            let jsonData = await response.json();
            let errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            return { error: errorMessage }
        }

        const json = await response.json();
        return json.grades;

    } catch (e) {
        return { error: e.message };
    }
}