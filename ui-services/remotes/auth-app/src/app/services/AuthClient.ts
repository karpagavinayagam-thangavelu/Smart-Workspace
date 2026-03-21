import Axios from "axios";

export const AuthClient = Axios.create({
    baseURL: process.env['NX_AUTH_API_URL'] || "http://localhost:3333",
});
