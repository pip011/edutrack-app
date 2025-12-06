import { PUBLIC_API_URL } from '$env/static/public';

export const load = async ({fetch, depends}) => {
    depends('app:subjects');
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/subjects`, {
            credentials: 'include'
        });

        if (!response.ok) {
            return { error: 'Ошибка загрузки предметов' };
        }

        const json = await response.json();
        return { subjects: json.subjects };

    } catch (e) {
        return { error: e.message };
    }
};