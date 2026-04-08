const { Client } = require('pg');

export default async function handler(req, res) {
    // Conexión usando la variable de entorno que pusiste en Vercel
    const client = new Client({
        connectionString: process.env.DATABASE_URL,
        ssl: { rejectUnauthorized: false }
    });

    try {
        await client.connect();
        const { email, password, accion } = req.body;

        // --- LÓGICA DE REGISTRO ---
        if (accion === "registro") {
            await client.query(
                'INSERT INTO usuarios (email, password) VALUES ($1, $2)', 
                [email, password]
            );
            return res.status(200).json({ mensaje: "Registro exitoso" });
        }

        // --- LÓGICA DE LOGIN ---
        if (accion === "login") {
            const result = await client.query(
                'SELECT * FROM usuarios WHERE email = $1 AND password = $2', 
                [email, password]
            );
            if (result.rows.length > 0) {
                return res.status(200).json({ 
                    mensaje: "Bienvenido", 
                    puntos: result.rows[0].puntos 
                });
            } else {
                return res.status(401).json({ mensaje: "Usuario o clave incorrectos" });
            }
        }

        // --- LÓGICA DE RECUPERACIÓN (BASE) ---
        if (accion === "recuperar") {
            // Aquí podrías integrar un servicio de correos como SendGrid o Resend
            return res.status(200).json({ mensaje: "Instrucciones enviadas al correo" });
        }

    } catch (err) {
        return res.status(500).json({ error: err.message });
    } finally {
        await client.end();
    }
}
