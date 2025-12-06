import { PUBLIC_API_URL } from '$env/static/public';

export const load = async ({fetch, depends}) => {
    depends("app:groups")
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups`, {
            credentials: 'include'
        });

        if (!response.ok) {
            return { error: 'Ошибка загрузки групп' };
        }

        const json = await response.json();
        return { groups: json.groups };

    } catch (e) {
        return { error: e.message };
    }
};