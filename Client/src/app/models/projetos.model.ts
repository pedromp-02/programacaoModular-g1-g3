export class Participante {
    public matricula!: string;
    public nome!: string;
    public email!: string;
    public cargaHorariaSemanal!: number;
}

export class ParticipanteAPI {
    public matricula!: string;
    public cargaHorariaSemanal!: number;

    public fillData(participante: Participante) {
        this.matricula = participante.matricula;
        this.cargaHorariaSemanal = participante.cargaHorariaSemanal;
    }
}

export class Projeto {
    public _id!: string;
    public nome!: string;
    public descricao!: string;
    public dataInicio!: string;
    public dataFim!: string;
    public suaCargaHoraria!: string;
    public participantes!: Array<Participante>;

    public fillBlank() {
        this.nome = '';
        this.descricao = '';
        this.dataInicio = '00/00/0000';
        this.dataFim = '00/00/0000';
        this.suaCargaHoraria = '';
        this.participantes = new Array<Participante>();
    }
}