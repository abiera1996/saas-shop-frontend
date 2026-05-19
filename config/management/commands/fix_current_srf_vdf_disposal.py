from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory, ServiceProvider, VDF, Supplier, SRF, SRFApproveHistory, SRFApprover, VDFApproveHistory, VDFApprover

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        # Complete 
        srfs = SRF.objects.filter(status='complete')
        for srf in srfs:
            if not srf.requesting_unit.branch.is_manila:
                approval_srf_type = 'default' 
            else:
                approval_srf_type = 'tfleet' 
            srf.approval_srf_type = approval_srf_type
            srf.save()
            history = SRFApproveHistory.objects.filter(srf=srf)
            if not history.exists():
                if srf.endorsed_by_bm:
                    SRFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        srf=srf,
                        user_role_name="Branch Manager",
                        approve_by=srf.endorsed_by_bm,
                        approval_date=srf.endorsed_date_bm,
                        comment=srf.endorsed_by_bm_comment
                    )

                if srf.approved_reject_by_group_head:
                    SRFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        srf=srf,
                        user_role_name="Group Head",
                        approve_by=srf.approved_reject_by_group_head,
                        approval_date=srf.approved_reject_date_group_head,
                        comment=srf.approved_group_head_comment
                    )

                if srf.endoresed_by_tfleet_personnel:
                    SRFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        srf=srf,
                        user_role_name="Tfleet Personnel",
                        approve_by=srf.endoresed_by_tfleet_personnel,
                        approval_date=srf.endoresed_date_tfleet_personnel,
                        comment=srf.endoresed_by_tfleet_personnel_comment
                    )
                
                if srf.approved_reject_by_tfleet_manager:
                    SRFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        srf=srf,
                        user_role_name="Tfleet Manager",
                        approve_by=srf.approved_reject_by_tfleet_manager,
                        approval_date=srf.approved_reject_date_tfleet_manager,
                        comment=srf.approved_by_tfleet_manager_comment
                    )

                if srf.complete_by_tfleet_personnel:
                    SRFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        srf=srf,
                        user_role_name="Tfleet Personnel",
                        approve_by=srf.complete_by_tfleet_personnel,
                        approval_date=srf.complete_date_tfleet_personnel,
                        comment=srf.approved_by_tfleet_manager_comment
                    )

        srfs = SRF.objects.exclude(status='complete') 
        for srf in srfs:
            history = SRFApproveHistory.objects.filter(srf=srf)
            if not history.exists():
                if not srf.requesting_unit.branch.is_manila:
                    approval_srf_type = 'default' 
                else:
                    approval_srf_type = 'tfleet' 
                srf.approval_srf_type = approval_srf_type
                srf.status = 'pending'
                srf.save()
        
        
        vdfs = VDF.objects.filter(status='approved')
        for vdf in vdfs:
            if vdf.branch.is_manila or vdf.reason_for_rental == 'Replacement of breakdown T-fleet vehicle':
                approval_vdf_type = 'tfleet' 
            else:
                approval_vdf_type = 'default' 
            vdf.approval_vdf_type = approval_vdf_type
            vdf.save()
            history = VDFApproveHistory.objects.filter(vdf=vdf)
            if not history.exists():
                if vdf.endorsed_by_bm:
                    VDFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        vdf=vdf,
                        user_role_name="Branch Manager",
                        approve_by=vdf.endorsed_by_bm,
                        approval_date=vdf.endorsed_date_bm,
                        comment=vdf.endorsed_by_bm_comment
                    )

                if vdf.approved_reject_by_group_head:
                    VDFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        vdf=vdf,
                        user_role_name="Group Head",
                        approve_by=vdf.approved_reject_by_group_head,
                        approval_date=vdf.approved_reject_date_group_head,
                        comment=vdf.approved_reject_by_group_head_comment
                    )

                if vdf.approved_reject_by_tfleet_personnel:
                    VDFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        vdf=vdf,
                        user_role_name="Tfleet Personnel",
                        approve_by=vdf.approved_reject_by_tfleet_personnel,
                        approval_date=vdf.approved_reject_date_tfleet_personnel,
                        comment=vdf.approved_reject_by_tfleet_personnel_comment
                    )
                
                if vdf.approved_reject_by_tfleet_manager:
                    VDFApproveHistory.objects.get_or_create(
                        type = 'approve',
                        vdf=vdf,
                        user_role_name="Tfleet Manager",
                        approve_by=vdf.approved_reject_by_tfleet_manager,
                        approval_date=vdf.approved_reject_date_tfleet_manager,
                        comment=vdf.approved_by_tfleet_manager_comment
                    )
        vdfs = VDF.objects.exclude(status='approved') 
        for vdf in vdfs:
            history = VDFApproveHistory.objects.filter(vdf=vdf)
            if not history.exists():
                if vdf.branch.is_manila or vdf.reason_for_rental == 'Replacement of breakdown T-fleet vehicle':
                    approval_vdf_type = 'tfleet' 
                else:
                    approval_vdf_type = 'default' 
                vdf.approval_vdf_type = approval_vdf_type
                vdf.status = 'pending'
                vdf.save()
        
        srfs = SRF.objects.all()
        for srf in srfs:
            sequence = 1
            for history in SRFApproveHistory.objects.filter(srf=srf).order_by('approval_date'):
                history.sequence = sequence
                history.save()
                sequence += 1
        srfs = VDF.objects.all()
        for srf in srfs:
            sequence = 1
            for history in VDFApproveHistory.objects.filter(vdf=srf).order_by('approval_date'):
                history.sequence = sequence
                history.save()
                sequence += 1
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

