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
}