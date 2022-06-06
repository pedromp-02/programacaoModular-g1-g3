export class Participante {
    public matricula!: string;
    public nome!: string;
    public email!: string;
    public cargaHorariaSemanal!: number;
}

export class Projeto {
    public _id!: string;
    public nome!: string;
    public descricao!: string;
    public dataInicio!: string;
    public dataFim!: string;
    public suaCargaHoraria!: string;
    public participantes!: Array<Participante>;
}