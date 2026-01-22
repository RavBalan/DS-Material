Begin Tran A
--Commit Tran A
--RollBack Tran A
Declare @MerchantID			Bigint	= (Select MerchantID From Merchant Where MerchantKey = '0000-8964-0001-5423')
Declare @TenantID           Bigint	= ( Select TenantID From Tenant Where TenantKey = '7891-8964-0001-5423')
Declare @VendorID           Bigint	= ( Select VendorID From Vendor Where VendorCode = 'KS-KTA' )
Declare @DocumentBillTypeID Bigint	= ( select DocumentBillTypeID from DocumentBillType Where DocumentBillType = 'TOLL')

Declare @DocumentTemplateID Bigint ,@DocumentTemplateName Varchar(100), @TemplateNumber varchar(100);
										Select top 1 @DocumentTemplateID =  DocumentTemplateID, @DocumentTemplateName= TemplateName, @TemplateNumber = TemplateNumber 
										From DocumentTemplate 
										Where TemplateName = 'KS-KTA' And VendorID = @VendorID 

Declare @Validation Bigint = ( Select top 1 DocumentTemplateID From DataTransformationRule Where DocumentTemplateID = @DocumentTemplateID )

print @Validation
If  IsNull(@Validation,1) = 1

Begin
	INSERT INTO dbo.DataTransformationRule
				(	
					DocumentTemplateID ,MerchantID,TenantID,VendorID,DocumentBillTypeID,TemplateNumber,TemplateName,DocumentField,DocumentFieldFormat,
					AIField,DocumentFieldType,Operation,RecordType,IsActive,IsRegex,FieldExpression,FieldIndex,IsField,IsDerived,CreatedDateTime
				)
	VALUES
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'PlateState',NULL,'LicenseState','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'PlateNumber',NULL,'LicensePlate','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'BillNumber',NULL,'DocumentId','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'BillDate',NULL,'InvoiceDate','Date','Direct','BILL',1,1,'/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'DueDate',NULL,'DueDate','Date','Direct','BILL',1,1,'/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'CheckMailingAddress',NULL,'VendorName','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'VendorName',NULL,'VendorName','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalTransactionAmount','PreviousBalanceDue + NewCharges',NULL,'Money','Calculate','BILL',1,1,'/[x^\s]/',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalLateFeesAmount',NULL,Null,'Money','Direct','BILL',1,0,NULL,NULL,0,0,GetDate()), -- If IsField is 0 AI Field Should Be Null Not a ZERO 
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalFeeAmount2',NULL,'0','Money','Direct','BILL',1,0,NULL,NULL,0,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalFeeAmount1',NULL,'0','Money','Direct','BILL',1,0,NULL,NULL,0,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalBillAmount',NULL,'TotalAmountDue','Money','Direct','BILL',1,1,'/[^\d.]/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'LoginURL',NULL,'VendorWebsite','Text','Direct','BILL',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'PlateNumber',NULL,'LicenseState','Text','Direct','TRANSACTION',1,1,'/^\s+|\s+$/g',NULL,1,1,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'PlateState',NULL,'LicensePlate','Text','Direct','TRANSACTION',1,1,'/^\s+|\s+$/g',NULL,1,1,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionAgencyState',NULL,'VendorState','Text','Direct','TRANSACTION',1,1,'/^\s+|\s+$/g',NULL,1,1,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionNumber',NULL,'DocumentId','Text','Direct','TRANSACTION',1,1,'/^\s+|\s+$/g',NULL,1,1,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionDate',NULL,'EntryDate','Date','Direct','TRANSACTION',1,1,'/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionTime',NULL,'EntryTime','Time','Direct','TRANSACTION',1,1,'/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionLocation',NULL,'EntryLocation','Text','Direct','TRANSACTION',1,1,'/^\s+|\s+$/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TransactionAmount',NULL,'TollAmount','Money','Direct','TRANSACTION',1,1,'/[^\d.]/g',NULL,1,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'FeeAmount1',NULL,'0','Money','Direct','TRANSACTION',1,1,NULL,NULL,0,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'FeeAmount2',NULL,'0','Money','Direct','TRANSACTION',1,1,NULL,NULL,0,0,GetDate()),
			(@DocumentTemplateID, @MerchantID, @TenantID, @VendorID, @DocumentBillTypeID, @TemplateNumber, @DocumentTemplateName,'TotalAmount',NULL,'TollAmount','Money','Direct','TRANSACTION',1,1,'/[^\d.]/g',NULL,1,0,GETDATE());
		
	Select * From DataTransformationRule Where DocumentTemplateID = @DocumentTemplateID
End
Else
Begin
	Select convert(varchar(10),@DocumentTemplateID) +' '+ @DocumentTemplateName +'   Template Already Exists'
End