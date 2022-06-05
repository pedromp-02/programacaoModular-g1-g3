import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorIntl } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppService } from './app.service';
import { DadosPessoaisComponent } from './dados-pessoais/dados-pessoais.component';
import { FuncionariosComponent } from './funcionarios/funcionarios.component';
import { ProjetosComponent } from './projetos/projetos.component';

/**
 * Função responsável por traduzir a paginação dos grids.
 */
export function getPtPaginatorIntl() {
    const ptRange = (page: number, pageSize: number, length: number) => {
        if (length == 0 || pageSize == 0) {
            return `0 de ${length}`;
        }

        length = Math.max(length, 0);

        const startIndex = page * pageSize;
        const endIndex = startIndex < length ? Math.min(startIndex + pageSize, length) : startIndex + pageSize;

        return `${startIndex + 1} - ${endIndex} de ${length}`;
    };

    const paginatorIntl = new MatPaginatorIntl();
    paginatorIntl.itemsPerPageLabel = 'Itens por página:';
    paginatorIntl.nextPageLabel = 'Próxima';
    paginatorIntl.previousPageLabel = 'Anterior';
    paginatorIntl.firstPageLabel = 'Primeira página';
    paginatorIntl.lastPageLabel = 'Última página';
    paginatorIntl.getRangeLabel = ptRange;

    return paginatorIntl;
}

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        FormsModule,
        HttpClientModule,
        BrowserAnimationsModule,
        MatButtonModule,
        MatFormFieldModule,
        MatInputModule,
        MatIconModule,
        MatSnackBarModule,
        MatTableModule,
        MatProgressSpinnerModule,
        MatTabsModule,
        AppRoutingModule
    ],
    declarations: [
        AppComponent,
        DadosPessoaisComponent,
        FuncionariosComponent,
        ProjetosComponent
    ],
    providers: [
        AppService,
        {
            provide: MatPaginatorIntl,
            useValue: getPtPaginatorIntl()
        }
    ],
    bootstrap: [AppComponent]
})

export class AppModule { }
