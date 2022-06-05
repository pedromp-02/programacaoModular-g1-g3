import { Usuario } from "./usuario.model";

export class Login {
    constructor (
        public message: string,
        public auth: string,
        public user: Usuario
    ) { }

    public isSuccessLogin() {
        return this.message === undefined && this.auth !== undefined && typeof this.auth === 'string' && typeof this.user === 'object';
    }
}