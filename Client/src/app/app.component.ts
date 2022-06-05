import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppService } from './app.service';
import { Usuario } from './models/usuario.model';

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
    public userLoginData: string = '';
    public userData!: Usuario;

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

    }

    /**
     * Função responsável por exibir e ocultar a modal de login
     */
    public toggleLogin() {
        this.showLogin = !this.showLogin;
    }

    /**
     * Função responsável por enviar a requisição de login
     */
    public async doLogin() {
        const loginData = await this.appService.login(this.formLoginEmail, this.formLoginSenha);

        if (loginData.isSuccessLogin()) {
            this.userData = loginData.user;
            this.appService.setJWT(loginData.auth);

            const data = new Date();
            this.userLoginData = `${data.getHours()}:${data.getMinutes()}`
            this.userIsLogged = true;

            this.showLogin = false;
            this.formLoginEmail = '';
            this.formLoginSenha = '';

            this.snackBar.open(`Bem vindo(a) ao sistema, ${loginData.user?.nome}`, 'Fechar');
        }
        else {
            const error: any = loginData;
            const message = error.error === undefined ? 'Usuário ou senha inválidos.' : error.error.message.toString();

            this.userIsLogged = false;
            this.snackBar.open(message, 'Fechar');
        }
    }

    /**
     * Função responsável por sair do sistema
     */
    public sair() {
        this.appService.setJWT('');

        this.userIsLogged = false;
        this.userLoginData = '';
        this.userData = new Usuario('', '', '', '', '', false)
    }
}
