import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Usuario } from './models/usuario.model';
import { Login } from './models/login.model';
import { ParticipanteAPI, Projeto } from './models/projetos.model';

@Injectable({
    providedIn: 'root'
})

export class AppService {
    private apiUrl: string = environment.apiUrl;
    private authJWT: string = '';

    private funcionariosData!: Array<Usuario>;

    constructor(private httpClientModule: HttpClient) {
    }

    public setJWT(jwt: string) {
        this.authJWT = jwt;
    }

    public login(email: string, senha: string): Promise<Login> {
        try {
            return new Promise<Login>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .post<Login>(`${this.apiUrl}/login`, { email, senha })
                    .toPromise()
                    .then((loginData?: Login) => {
                        if (loginData === undefined) {
                            resolve(new Login('', '', undefined))
                        }
                        else {
                            resolve(new Login(loginData.message, loginData.auth,  loginData.user));
                        }
                    })
                    .catch((loginData?: Login) => {
                        if (loginData === undefined) {
                            resolve(new Login('', '', undefined))
                        }
                        else {
                            resolve(new Login(loginData.message, loginData.auth,  loginData.user));
                        }
                    });
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public getFuncionarios(): Promise<Array<Usuario>> {
        try {
            return new Promise<Array<Usuario>>((resolve, reject) => {
                if (Array.isArray(this.funcionariosData)) {
                    resolve(this.funcionariosData);
                    return;
                }    

                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .get<Array<Usuario>>(`${this.apiUrl}/funcionarios/user`,
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((funcionariosData: any) => {
                        this.funcionariosData = funcionariosData;
                        resolve(funcionariosData);
                    })
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public addFuncionario(dados: Usuario) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .put<any>(`${this.apiUrl}/funcionarios/add`, 
                    { 
                        nome: dados.nome,
                        usuario: dados.usuario,
                        email: dados.email,
                        cpf: dados.cpf,
                        cargo: dados.cargo,
                        salario: dados.salario,
                        dataAdmissao: dados.dataAdmissao,
                        dataNascimento: dados.dataNascimento,
                        endereco: dados.endereco,
                        dependentes: dados.dependentes,
                        senha: dados.senha
                    },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public editFuncionario(dados: Usuario) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .post<any>(`${this.apiUrl}/funcionarios/${dados._id}`, 
                    {
                        nome: dados.nome,
                        usuario: dados.usuario,
                        email: dados.email,
                        cpf: dados.cpf,
                        cargo: dados.cargo,
                        salario: dados.salario,
                        dataAdmissao: dados.dataAdmissao,
                        dataNascimento: dados.dataNascimento,
                        endereco: dados.endereco,
                        dependentes: dados.dependentes,
                        senha: dados.senha
                    },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public removeFuncionario(id: string) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .delete<any>(`${this.apiUrl}/funcionarios/${id}`,
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public getProjetos(): Promise<Array<Projeto>> {
        try {
            return new Promise<Array<Projeto>>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .get<Array<Projeto>>(`${this.apiUrl}/projetos/list`,
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public getProjetosUserLogado(): Promise<Array<Projeto>> {
        try {
            return new Promise<Array<Projeto>>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .get<Array<Projeto>>(`${this.apiUrl}/projetos/mine`,
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public addProjeto(projeto: Projeto) {
        try {
            return new Promise<any>((resolve, reject) => {
                let participantes: Array<ParticipanteAPI> = new Array<ParticipanteAPI>();

                for (let participante of projeto.participantes) {
                    let participanteAPIData = new ParticipanteAPI();
                    participanteAPIData.fillData(participante);

                    participantes.push(participanteAPIData);
                }

                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .put<any>(`${this.apiUrl}/projetos/add`, {
                        nome: projeto.nome,
                        descricao: projeto.descricao,
                        dataInicio: projeto.dataInicio,
                        dataFim: projeto.dataFim,
                        participantes
                    },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public editProjeto(projeto: Projeto) {
        try {
            return new Promise<any>((resolve, reject) => {
                let participantes: Array<ParticipanteAPI> = new Array<ParticipanteAPI>();

                for (let participante of projeto.participantes) {
                    let participanteAPIData = new ParticipanteAPI();
                    participanteAPIData.fillData(participante);

                    participantes.push(participanteAPIData);
                }

                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .post<any>(`${this.apiUrl}/projetos/${projeto._id}`, {
                        nome: projeto.nome,
                        descricao: projeto.descricao,
                        dataInicio: projeto.dataInicio,
                        dataFim: projeto.dataFim,
                        participantes
                    },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public removeProjeto(id: string) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .delete<any>(`${this.apiUrl}/projetos/${id}`,
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + this.authJWT
                        })
                    })
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }
}
