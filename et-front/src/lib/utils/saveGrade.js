import { PUBLIC_API_URL } from "$env/static/public";

export async function saveGrade({ studentId, day, grade, subjectId, month, year }, gradesMap) {
    const key = `${studentId}-${day}`;
    const existing = gradesMap.get(key);

    try {
        if (existing) {
            if (grade === null) {
                const res = await fetch(`${PUBLIC_API_URL}/api/grades/delete/${existing.id}`, { 
                    method: 'POST', 
                    credentials: 'include' 
                });

                const data = await res.json();
                if (!res.ok) {
                    return { error: data.detail || data.error || `HTTP ${res.status}` };
                }

                gradesMap.delete(key);
                return { success: true };
            } else if (existing.grade !== grade) {
                const res = await fetch(`${PUBLIC_API_URL}/api/grades/grade/${existing.id}`, {
                    method: 'PATCH',
                    credentials: 'include',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ grade })
                });

                const data = await res.json();
                if (!res.ok) {
                    return { error: data.detail || data.error || `HTTP ${res.status}` };
                }

                existing.grade = grade;
                gradesMap.set(key, existing);
                return { success: true };
            }
        } else {
            if (grade !== null) {
                const paddedMonth = String(month).padStart(2, "0");
                const paddedDay = String(day).padStart(2, "0");
                const isoDate = `${year}-${paddedMonth}-${paddedDay}`;

                const res = await fetch(`${PUBLIC_API_URL}/api/grades`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        student_id: studentId,
                        subject_id: subjectId,
                        date: isoDate,
                        grade
                    })
                });

                const data = await res.json();
                if (!res.ok) {
                    return { error: data.detail || data.error || `HTTP ${res.status}` };
                }

                gradesMap.set(key, data);
                return { success: true };
            }
        }

        return { success: true };
    } catch (e) {
        return { error: e.message || 'Unknown error' };
    }
}