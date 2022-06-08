import { Component, Input } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { Usuario } from '../models/usuario.model';

@Component({
    selector: 'app-dados-pessoais',
    templateUrl: './dados-pessoais.component.html',
    styleUrls: ['./dados-pessoais.component.scss']
})

export class DadosPessoaisComponent {
    @Input() userData!: Usuario;
    @Input() paddingBottom!: boolean;

    public gridData: MatTableDataSource<any> = new MatTableDataSource();
    public gridColumns: Array<any> = [];
    public gridColumnsToDisplay: Array<string> = [];

    constructor() { }

    ngOnInit() {
        this.createGridData();
    }

    private createGridData() {
        this.gridData.data = this.userData.dependentes;
        this.gridColumns = [
            { name: 'nome', display: 'Nome' },
            { name: 'parentesco', display: 'Parentesco' },
            { name: 'cpf', display: 'CPF' }
        ];       
        this.gridColumnsToDisplay = this.gridColumns.map(col => col.name);
    }

    get salario() {
        return "R$ " + this.userData.salario.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    get endereco() {
        return this.userData.endereco.logradouro + ", " +
            this.userData.endereco.bairro + " - " +
            this.userData.endereco.cidade + " " +
            this.userData.endereco.estado + " (CEP " +
            this.userData.endereco.cep.toString().replace(/^([\d]{2})\.*([\d]{3})-*([\d]{3})/,"$1.$2-$3") + ")";
    }
}
