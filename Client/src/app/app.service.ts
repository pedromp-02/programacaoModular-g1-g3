import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Usuario } from './models/usuario.model';
import { Login } from './models/login.model';
import { Projeto } from './models/projetos.model';

@Injectable({
    providedIn: 'root'
})

export class AppService {
    private apiUrl: string = environment.apiUrl;

    constructor(private httpClientModule: HttpClient) {
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
                    .then((loginData: any) => resolve(loginData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public getFuncionarios(): Promise<Array<Usuario>> {
        try {
            return new Promise<Array<Usuario>>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .get<Array<Usuario>>(`${this.apiUrl}/funcionarios/user`)
                    .toPromise()
                    .then((funcionariosData: any) => resolve(funcionariosData))
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
                    .get<Array<Projeto>>(`${this.apiUrl}/projetos/user`)
                    .toPromise()
                    .then((projetosData: any) => resolve(projetosData))
                    .catch(e => resolve(e));
            });
        }
        catch (e) {
            return Promise.reject(e);
        }
    }

    public addProjeto(jwt: string, nome: string, descricao: string, participantes: Array<string>) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .put<any>(`${this.apiUrl}/projetos/add`, { nome, descricao, participantes },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + jwt
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

    public editProjeto(jwt: string, id: string, nome: string, descricao: string, participantes: Array<string>) {
        try {
            return new Promise<any>((resolve, reject) => {
                /**
                 * Busca os dados no servidor
                 */
                this.httpClientModule
                    .post<any>(`${this.apiUrl}/projetos/${id}`, { nome, descricao, participantes },
                    {
                        headers: new HttpHeaders ({
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': 'Bearer ' + jwt
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

    public removeProjeto(jwt: string, id: string) {
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
                            'Authorization': 'Bearer ' + jwt
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
