import { PUBLIC_API_URL } from '$env/static/public';

export async function checkAuth() {
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/auth/me`, {
            credentials: 'include'
        });

        if (response.ok) {
            const userData = await response.json();
            return userData;
        } else {
            return null;
        }
    } catch (e) {
        console.error('Auth check failed:', e);
        return null;
    }
}