import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Usuario } from './models/usuario.model';
import { Login } from './models/login.model';

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
}
