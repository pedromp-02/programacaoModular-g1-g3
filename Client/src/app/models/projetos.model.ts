export class Projeto {
    constructor(
        public _id: string,
        public nome: string,
        public descricao: string,
        public participantes: Array<string>) {

    }
}