import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {
  GiveFeedbackComponent,
  EnrolleesListComponent,
  LoginComponent,
  EnrolComponent,
  StatsComponent,
  SummariseFeedbackComponent,
  FeedbackAboutMeComponent,
  TalentManagerPanelComponent,
  AuthenticatedComponent,
  FeedbackHistoryViewComponent,
  RequestComponent
} from './components/views';

import { AuthGuardService, AnonGuardService, PendingChangesGuardService } from './guards';

const routes: Routes = [
  { path: '', redirectTo: '/feedback', pathMatch: 'full' },
  { path: 'login', canActivate: [AnonGuardService], component: LoginComponent },
  {
    path: '',
    component: AuthenticatedComponent,
    canActivate: [AuthGuardService],
    children: [
      { path: 'enrol', component: EnrolComponent },
      { path: 'feedback-about-me', component: FeedbackAboutMeComponent },
      { path: 'feedback', component: EnrolleesListComponent },
      { path: 'invite-outside-reviewers', component: RequestComponent },
      {
        path: 'feedback/:username',
        canDeactivate: [PendingChangesGuardService],
        component: GiveFeedbackComponent
      },
      { path: 'team-feedback', component: StatsComponent, data: {isCompanyWide: false} },
      { path: 'company-feedback', component: StatsComponent, data: {isCompanyWide: true}},
      {
        path: 'team-feedback/:username/summarise',
        canDeactivate: [PendingChangesGuardService],
        component: SummariseFeedbackComponent
      },
      {
        path: 'team-feedback/:username/history',
        component: FeedbackHistoryViewComponent
      },
      { path: 'talent-manager-panel', component: TalentManagerPanelComponent }

    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
