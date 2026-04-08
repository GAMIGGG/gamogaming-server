const { Client } = require('pg');

export default async function handler(req, res) {
    const client = new Client({
        connectionString: process.env.DATABASE_URL,
        ssl: { rejectUnauthorized: false }
    });

    try {
        await client.connect();
        const { email, password, accion } = req.body;

        if (accion === "registro") {
            await client.query('INSERT INTO usuarios (email, password) VALUES ($1, $2)', [email, password]);
            return res.status(200).json({ mensaje: "Usuario creado con éxito" });
        } 
        
        if (accion === "login") {
            const result = await client.query('SELECT * FROM usuarios WHERE email = $1 AND password = $2', [email, password]);
            if (result.rows.length > 0) {
                return res.status(200).json({ mensaje: "Bienvenido", token: "usuario_valido" });
            } else {
                return res.status(401).json({ mensaje: "Datos incorrectos" });
            }
        }

    } catch (err) {
        return res.status(500).json({ error: err.message });
    } finally {
        await client.end();
    }
}
