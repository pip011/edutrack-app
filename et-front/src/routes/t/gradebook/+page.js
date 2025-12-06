import { loadGroups, loadSubjectsForTeacher, getIdForTeacher } from "$lib/utils/teacherGradebook";

export async function load({depends, fetch}) {
    depends("app:gradebook")

    let teacher = await getIdForTeacher()
    if (teacher.error) {
        return {error: teacher.error}
    }

    let subjects = await loadSubjectsForTeacher(teacher.id);
    if (subjects.error) {
        return {error: subjects.error}
    }

    let groups = await loadGroups()
    if (groups.error) {
        return {error: groups.error}
    }

    return {subjects: subjects, 
            groups: groups
    }
}