export class Endereco {
    public cep!: number;
    public logradouro!: string;
    public bairro!: string;
    public cidade!: string;
    public estado!: string;
}

export class Dependente {
    public nome!: string;
    public parentesco!: string;
    public cpf!: string;
}

export class Usuario {
    public _id!: string;
    public nome!: string;
    public email!: string;
    public usuario!: string;
    public cargo!: string;
    public salario!: number;
    public dataAdmissao!: string;
    public dataNascimento!: string;
    public cpf!: string;
    public senha!: string;
    public endereco!: Endereco;
    public dependentes!: Array<Dependente>;
    public possuiPermissaoRH!: boolean;

    public fillBlank() {
        this.nome = '';
        this.email = '';
        this.usuario = '';
        this.cargo = '';
        this.salario = 0;
        this.dataAdmissao = '00/00/0000';
        this.dataNascimento = '00/00/0000';
        this.cpf = '000.000.000-00';
        this.senha = '';

        this.endereco = new Endereco();
        this.endereco.logradouro = '';
        this.endereco.bairro = '';
        this.endereco.cep = 0;
        this.endereco.cidade = '';
        this.endereco.estado = '';

        this.dependentes = new Array<Dependente>();
    }
}