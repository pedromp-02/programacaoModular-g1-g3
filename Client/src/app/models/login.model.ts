import { Usuario } from "./usuario.model";

export class Login {
    constructor (
        public message: string,
        public auth: string,
        public user: Usuario
    ) { }
}