import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppService } from './app.service';
import { Login } from './models/login.model';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent {
    /**
     * Controla se o usuario esta logado
     */
    public userIsLogged: boolean = false;
    public userData: Login;

    /**
     * Controla a exibicao da modal de login
     */
    public showLogin: boolean = false;
    public hidePassword: boolean = true;

    /**
     * Variaveis para o login
     */
    public formLoginEmail = '';
    public formLoginSenha = '';

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) {

        this.userData = new Login();
    }

    public toggleLogin() {
        this.showLogin = !this.showLogin;
    }

    /**
     * Função responsável por enviar a requisição de login
     */
    public async doLogin() {
        const loginData = await this.appService.login(this.formLoginEmail, this.formLoginSenha);

        if (loginData.auth !== null && loginData.auth !== undefined && typeof loginData.auth === 'string') {
            this.userIsLogged = true;
            this.userData = loginData;

            this.snackBar.open(`Bem vindo(a) ao sistema, ${loginData.nome}`, 'Fechar');
        }
        else {
            const error: any = loginData;
            const message = error.error === undefined ? 'Usuário ou senha inválidos.' : error.error.message.toString();

            this.userIsLogged = false;
            this.snackBar.open(message, 'Fechar');
        }
    }
}
