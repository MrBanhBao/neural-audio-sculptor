const HOST: string | unknown = '127.0.0.1';
const PORT: number | unknown = 8000;

const webSocketUrl = `ws://${HOST}:${PORT}`

export const wsRoutineUrl = `${webSocketUrl}/api/diffusion/ws/routine`