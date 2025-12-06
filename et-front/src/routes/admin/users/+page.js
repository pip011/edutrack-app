import { PUBLIC_API_URL } from '$env/static/public';

export const load = async ({fetch, depends}) => {
    depends('app:users');
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/users`, {
            credentials: 'include'
        });

        if (!response.ok) {
            return { error: 'Ошибка загрузки пользователей' };
        }

        const json = await response.json();
        return { users: json.users };

    } catch (e) {
        return { error: e.message };
    }
};